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

    template_path = DOCS / "index.template.html"
    html_path = DOCS / "index.html"
    if template_path.exists():
        # Data loads via fetch(concepts.json / scenarios.json / playbook.json)
        html_path.write_text(template_path.read_text())

    with_snip = sum(1 for c in all_concepts if c.get("snippet"))
    with_sym = sum(1 for c in all_concepts if c.get("symptom"))
    with_rel = sum(1 for c in all_concepts if c.get("related"))
    print(
        f"Wrote {len(all_concepts)} concepts ({len(must)} must-know, "
        f"{with_snip} snippets, {with_sym} symptoms, {with_rel} related, "
        f"{len(scenarios)} scenarios, {len(playbook)} playbook)"
    )


if __name__ == "__main__":
    main()
