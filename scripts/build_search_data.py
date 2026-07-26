#!/usr/bin/env python3
"""Merge markdown concepts + enrichment + tags → docs/concepts.json and docs/index.html."""

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
    json_path = DOCS / "concepts.json"
    payload = json.dumps(all_concepts, indent=2)
    json_path.write_text(payload + "\n")

    must = sorted(
        [c for c in all_concepts if c.get("mustKnow")],
        key=lambda x: x["mustKnow"],
    )
    must_md = ["# Must-know 30", "", "Start here. Learn these before the long tail.", ""]
    for c in must:
        tags = ", ".join(f"`{t}`" for t in c.get("tags", []))
        must_md.append(f"{c['mustKnow']}. **{c['name']}** — {c['definition']}")
        if tags:
            must_md.append("")
            must_md.append(f"Tags: {tags}")
        if c.get("snippet"):
            must_md.append("")
            must_md.append("```")
            must_md.append(c["snippet"])
            must_md.append("```")
        if c.get("symptom"):
            must_md.append("")
            must_md.append(f"*In prod:* {c['symptom']}")
        must_md.append("")
    (ROOT / "MUST_KNOW_30.md").write_text("\n".join(must_md))

    template_path = DOCS / "index.template.html"
    html_path = DOCS / "index.html"
    if template_path.exists():
        html = template_path.read_text().replace("__CONCEPTS_JSON__", payload)
        html_path.write_text(html)
    elif html_path.exists():
        html = html_path.read_text()
        html = re.sub(
            r'<script type="application/json" id="concepts-data">.*?</script>',
            lambda _m: f'<script type="application/json" id="concepts-data">\n{payload}\n  </script>',
            html,
            count=1,
            flags=re.S,
        )
        html_path.write_text(html)

    tag_counts = {}
    for c in all_concepts:
        for t in c["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    print(f"Wrote {len(all_concepts)} concepts ({len(must)} must-know)")
    print("Tags:", ", ".join(f"{k}={v}" for k, v in sorted(tag_counts.items())))


if __name__ == "__main__":
    main()
