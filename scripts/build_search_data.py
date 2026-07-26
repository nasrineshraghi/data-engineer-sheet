#!/usr/bin/env python3
"""Merge markdown + enrichment + tags → docs/concepts.json and docs/index.html."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "scripts"))
from tags import CATEGORY_TAGS, CONCEPT_TAG_EXTRAS  # noqa: E402

CATEGORIES = [
    ("01-database-sql", "Database & SQL Concepts"),
    ("02-spark-internals", "Spark Internals"),
    ("03-data-warehouse", "Data Warehouse Concepts"),
    ("04-data-lake-lakehouse", "Data Lake & Lakehouse"),
    ("05-distributed-systems", "Distributed Systems"),
    ("06-streaming", "Streaming"),
    ("07-pipeline-design", "Pipeline Design"),
    ("08-performance-tuning", "Performance Tuning"),
    ("09-data-quality-governance", "Data Quality & Governance"),
    ("10-cloud-storage", "Cloud & Storage"),
    ("11-devops", "DevOps for Data"),
    ("12-cdc-scd", "CDC & SCD"),
    ("13-dbt", "dbt"),
    ("14-kafka", "Kafka"),
    ("15-airflow", "Airflow"),
    ("16-cost-optimization", "Cost Optimization"),
    ("17-snowflake", "Snowflake"),
    ("18-clinical-data", "Clinical Data — Meds & Labs"),
    ("19-api", "APIs for Data Engineers"),
    ("20-file-formats", "File Formats"),
    ("21-data-modeling", "Data Modeling Patterns"),
]


def parse_file(path: Path, category: str, slug: str) -> list[dict]:
    text = path.read_text()
    concepts = []
    for part in re.split(r"\n### ", text)[1:]:
        lines = part.strip().split("\n")
        name = lines[0].strip()
        body = "\n".join(lines[1:])
        def_match = re.search(r"\*\*Definition:\*\*\s*(.+?)(?=\n\n|\n\*\*)", body, re.S)
        why_match = re.search(r"\*\*Why it matters:\*\*\s*(.+?)(?=\n\n|\n\*\*)", body, re.S)
        ex_match = re.search(
            r"\*\*Example:\*\*\s*(.+?)(?=\n\n\*\*Remember|\n\*\*Remember)", body, re.S
        )
        rem_match = re.search(r"\*\*Remember:\*\*\s*(.+?)(?=\n---|\Z)", body, re.S)
        remember = []
        if rem_match:
            remember = [
                re.sub(r"^-\s*", "", line.strip())
                for line in rem_match.group(1).split("\n")
                if line.strip().startswith("-")
            ]
        concepts.append(
            {
                "name": name,
                "category": category,
                "categorySlug": slug,
                "file": f"{slug}/concepts.md",
                "definition": re.sub(r"\s+", " ", (def_match.group(1).strip() if def_match else "")),
                "why": re.sub(r"\s+", " ", (why_match.group(1).strip() if why_match else "")),
                "example": (ex_match.group(1).strip() if ex_match else ""),
                "remember": remember,
            }
        )
    return concepts


def build_tags(name: str, slug: str, must_know, enrichment_tags) -> list[str]:
    tags: set[str] = set(CATEGORY_TAGS.get(slug, []))
    tags.update(CONCEPT_TAG_EXTRAS.get(name, []))
    tags.update(enrichment_tags or [])
    if must_know:
        tags.add("interview")
    return sorted(tags)


def main() -> None:
    enrichment = {}
    enrich_path = DOCS / "enrichment.json"
    if enrich_path.exists():
        enrichment = json.loads(enrich_path.read_text())

    scenarios = []
    scenarios_path = DOCS / "scenarios.json"
    if scenarios_path.exists():
        scenarios = json.loads(scenarios_path.read_text())

    playbook = []
    playbook_path = DOCS / "playbook.json"
    if playbook_path.exists():
        playbook = json.loads(playbook_path.read_text())

    all_concepts: list[dict] = []
    for slug, category in CATEGORIES:
        all_concepts.extend(parse_file(ROOT / slug / "concepts.md", category, slug))

    for c in all_concepts:
        extra = enrichment.get(c["name"], {})
        c["mustKnow"] = extra.get("mustKnow")
        c["snippet"] = extra.get("snippet", "")
        c["related"] = extra.get("related", [])
        c["symptom"] = extra.get("symptom", "")
        c["tags"] = build_tags(
            c["name"], c["categorySlug"], c["mustKnow"], extra.get("tags")
        )

    DOCS.mkdir(exist_ok=True)
    payload = json.dumps(all_concepts, indent=2)
    (DOCS / "concepts.json").write_text(payload + "\n")
    scenarios_payload = json.dumps(scenarios, indent=2)
    playbook_payload = json.dumps(playbook, indent=2)
    # Works with file:// (Cursor preview) and http — no fetch required
    (DOCS / "data.js").write_text(
        "window.DE_CONCEPTS = "
        + payload
        + ";\nwindow.DE_SCENARIOS = "
        + scenarios_payload
        + ";\nwindow.DE_PLAYBOOK = "
        + playbook_payload
        + ";\n"
    )

    must = sorted(
        [c for c in all_concepts if c.get("mustKnow")],
        key=lambda x: x["mustKnow"],
    )
    must_md = [
        "# Must-know 30",
        "",
        "Do **[The most important 10](ESSENTIALS.md)** first. These 30 are the next layer.",
        "",
        "Readable UI: [Essentials](docs/index.html?mode=essentials) · [Must 30](docs/index.html?mode=must) · [Prod playbook](docs/index.html?mode=prod)",
        "",
    ]
    for c in must:
        must_md.append(f"## {c['mustKnow']}. {c['name']}")
        must_md.append("")
        must_md.append(c["definition"])
        must_md.append("")
        if c.get("snippet"):
            must_md.append("```")
            must_md.append(c["snippet"])
            must_md.append("```")
            must_md.append("")
        if c.get("symptom"):
            must_md.append(f"**In prod:** {c['symptom']}")
            must_md.append("")
        must_md.append("---")
        must_md.append("")
    (ROOT / "MUST_KNOW_30.md").write_text("\n".join(must_md))

    # Quick reference markdown + HTML table
    from html import escape as html_escape

    ordered = sorted(all_concepts, key=lambda c: (c["category"], c["name"].lower()))
    md_lines = [
        "# Quick reference (summary table)",
        "",
        "One-page cheat sheet: keyword · section · definition · example.",
        "",
        "**Prefer the interactive HTML table:** https://nasrineshraghi.github.io/data-engineer-sheet/table.html",
        "",
        f"**{len(ordered)} concepts** · [Study app](https://nasrineshraghi.github.io/data-engineer-sheet/) · [Local HTML](docs/table.html)",
        "",
        "| Keyword | Section | Definition | Example |",
        "|---|---|---|---|",
    ]
    for c in ordered:
        name = c["name"].replace("|", "\\|")
        cat = c["category"].replace("|", "\\|")
        definition = " ".join((c.get("definition") or "").split()).replace("|", "\\|")
        example = " ".join((c.get("example") or "").split()).replace("|", "\\|")
        if len(definition) > 160:
            definition = definition[:157] + "…"
        if len(example) > 180:
            example = example[:177] + "…"
        md_lines.append(f"| **{name}** | {cat} | {definition} | {example} |")
    (ROOT / "QUICK_REF.md").write_text("\n".join(md_lines) + "\n")

    rows_html = []
    current_cat = None
    for c in ordered:
        if c["category"] != current_cat:
            if current_cat is not None:
                rows_html.append("</section>")
            current_cat = c["category"]
            rows_html.append(
                f'<section class="section" data-section-block="{html_escape(current_cat)}">'
                f'<h2 class="section-title">{html_escape(current_cat)}</h2>'
            )
        example = (c.get("example") or "").strip()
        rows_html.append(
            f'<article class="card" data-section="{html_escape(c["category"])}">'
            f'<div class="card-top">'
            f'<h3 class="kw">{html_escape(c["name"])}</h3>'
            f'<span class="pill">{html_escape(c["category"])}</span>'
            f"</div>"
            f'<p class="def">{html_escape(c.get("definition") or "")}</p>'
            f'<div class="ex-label">Example</div>'
            f'<pre class="ex">{html_escape(example)}</pre>'
            f"</article>"
        )
    if current_cat is not None:
        rows_html.append("</section>")
    cats = sorted({c["category"] for c in ordered})
    cat_opts = "\n".join(
        f'<option value="{html_escape(c)}">{html_escape(c)}</option>' for c in cats
    )
    table_template = DOCS / "table.template.html"
    table_path = DOCS / "table.html"
    if table_template.exists():
        table_html = (
            table_template.read_text()
            .replace("__COUNT__", str(len(ordered)))
            .replace("__CAT_OPTS__", cat_opts)
            .replace("__ROWS__", "\n".join(rows_html))
        )
        table_path.write_text(table_html)

    # Static homepage (no JS) — always visible on GitHub Pages
    home_template = DOCS / "home.template.html"
    if home_template.exists():
        (DOCS / "index.html").write_text(home_template.read_text())

    # Static section pages (no JS) — Essentials / Prod / Must
    write_static_section_pages(all_concepts, must, playbook)

    # Interactive study app
    app_template = DOCS / "index.template.html"
    if app_template.exists():
        (DOCS / "app.html").write_text(app_template.read_text())

    with_snip = sum(1 for c in all_concepts if c.get("snippet"))
    with_sym = sum(1 for c in all_concepts if c.get("symptom"))
    with_rel = sum(1 for c in all_concepts if c.get("related"))
    print(
        f"Wrote {len(all_concepts)} concepts ({len(must)} must-know, "
        f"{with_snip} snippets, {with_sym} symptoms, {with_rel} related, "
        f"{len(scenarios)} scenarios, {len(playbook)} playbook); "
        f"pages: index + essentials + prod + must + table + app"
    )


def write_static_section_pages(
    all_concepts: list[dict], must: list[dict], playbook: list[dict]
) -> None:
    from html import escape as html_escape

    tpl_path = DOCS / "static-page.template.html"
    if not tpl_path.exists():
        return
    tpl = tpl_path.read_text()

    by_name = {c["name"]: c for c in all_concepts}
    essentials_names = [
        "Grain",
        "Idempotency",
        "Shuffle",
        "Partition Pruning",
        "Predicate Pushdown",
        "Cardinality",
        "Lazy Evaluation",
        "Job → Stage → Task",
        "At Least Once",
        "Freshness",
    ]
    why = {
        "Grain": "Know what one row means before you join or aggregate",
        "Idempotency": "Safe to retry = no duplicate mess",
        "Shuffle": "Moving data across the network is usually the expensive part",
        "Partition Pruning": "Date (or key) filters should skip whole folders of data",
        "Predicate Pushdown": "Filter early so you read less",
        "Cardinality": "Distinct counts drive join and group-by cost",
        "Lazy Evaluation": "Spark builds a plan; an action runs it",
        "Job → Stage → Task": "How to read the Spark UI when something is slow",
        "At Least Once": "Failures often mean duplicates unless you dedupe",
        "Freshness": "Green pipeline ≠ data is recent enough",
    }

    def render(page: str, **fields: str) -> None:
        html = tpl
        flags = {
            "essentials": "",
            "prod": "",
            "must": "",
            "api": "",
        }
        if page in flags:
            flags[page] = "on"
        html = (
            html.replace("__ON_ESSENTIALS__", flags["essentials"])
            .replace("__ON_PROD__", flags["prod"])
            .replace("__ON_MUST__", flags["must"])
            .replace("__ON_API__", flags["api"])
        )
        for k, v in fields.items():
            html = html.replace(f"__{k}__", v)
        (DOCS / f"{page}.html").write_text(html)

    # Essentials
    rows = []
    for i, name in enumerate(essentials_names, 1):
        c = by_name.get(name) or {}
        rows.append(
            "<tr>"
            f'<td class="n">{i}</td>'
            f'<td class="kw">{html_escape(name)}</td>'
            f"<td>{html_escape(c.get('definition') or '')}</td>"
            f"<td>{html_escape(why.get(name, c.get('why') or ''))}</td>"
            "</tr>"
        )
    essentials_body = (
        "<table><thead><tr><th>#</th><th>Concept</th><th>Definition</th>"
        "<th>Remember</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )
    render(
        "essentials",
        TITLE="DE Sheet — Essentials (10)",
        BANNER="#ea580c",
        BANNER_TEXT="ESSENTIALS · the only 10 to learn first",
        H1="Essentials (10)",
        SUB="Ignore the rest of the glossary until you can explain each of these in one sentence.",
        BODY=essentials_body,
    )

    # Prod playbook
    cards = []
    for item in playbook:
        concepts = ", ".join(html_escape(x) for x in item.get("concepts") or [])
        cards.append(
            '<article class="card">'
            f'<h2>See: {html_escape(item.get("see") or "")}</h2>'
            f'<p class="do"><strong>Do:</strong> {html_escape(item.get("do") or "")}</p>'
            f'<p class="concepts">Concepts: {concepts}</p>'
            f'<p class="habit"><strong>Habit:</strong> {html_escape(item.get("habit") or "")}</p>'
            "</article>"
        )
    render(
        "prod",
        TITLE="DE Sheet — Prod playbook",
        BANNER="#0f766e",
        BANNER_TEXT="PROD · symptom → action → concepts",
        H1="Prod playbook",
        SUB="Start from what you see in production, not from the topic list.",
        BODY="".join(cards) or "<p>No playbook entries.</p>",
    )

    # Must 30
    must_cards = []
    for c in must:
        symptom = (
            f'<p class="why">{html_escape(c.get("symptom") or "")}</p>'
            if c.get("symptom")
            else ""
        )
        must_cards.append(
            '<article class="card">'
            f'<h2>{c.get("mustKnow")}. {html_escape(c.get("name") or "")}</h2>'
            f'<p class="def">{html_escape(c.get("definition") or "")}</p>'
            f"{symptom}"
            "</article>"
        )
    render(
        "must",
        TITLE="DE Sheet — Must-know 30",
        BANNER="#ca8a04",
        BANNER_TEXT="MUST 30 · next layer after Essentials",
        H1="Must-know 30",
        SUB="Do Essentials first. These 30 are the next layer.",
        BODY="".join(must_cards) or "<p>No must-know entries.</p>",
    )

    # APIs
    api_concepts = [c for c in all_concepts if c.get("categorySlug") == "19-api"]
    api_cards = []
    for c in api_concepts:
        ex = html_escape((c.get("example") or "").strip())
        why = (
            f'<p class="why"><strong>Why:</strong> {html_escape(c.get("why") or "")}</p>'
            if c.get("why")
            else ""
        )
        example = f'<p class="do"><strong>Example:</strong> {ex}</p>' if ex else ""
        api_cards.append(
            '<article class="card">'
            f'<h2>{html_escape(c.get("name") or "")}</h2>'
            f'<p class="def">{html_escape(c.get("definition") or "")}</p>'
            f"{why}"
            f"{example}"
            "</article>"
        )
    render(
        "api",
        TITLE="DE Sheet — APIs for Data Engineers",
        BANNER="#0284c7",
        BANNER_TEXT="API · REST, auth, pagination, webhooks",
        H1="APIs for Data Engineers",
        SUB="How pipelines pull, push, and design HTTP APIs — contracts, retries, and incremental extracts.",
        BODY="".join(api_cards) or "<p>No API concepts.</p>",
    )


if __name__ == "__main__":
    main()
