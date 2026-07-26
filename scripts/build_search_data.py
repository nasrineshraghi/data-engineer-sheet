#!/usr/bin/env python3
"""Merge markdown concepts + enrichment → docs/concepts.json and embed in docs/index.html."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

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

    DOCS.mkdir(exist_ok=True)
    json_path = DOCS / "concepts.json"
    payload = json.dumps(all_concepts, indent=2)
    json_path.write_text(payload + "\n")

    # Also write must-know list for README / humans
    must = sorted(
        [c for c in all_concepts if c.get("mustKnow")],
        key=lambda x: x["mustKnow"],
    )
    must_md = ["# Must-know 30", "", "Start here. Learn these before the long tail.", ""]
    for c in must:
        must_md.append(f"{c['mustKnow']}. **{c['name']}** — {c['definition']}")
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

    html_path = DOCS / "index.html"
    if html_path.exists():
        html = html_path.read_text()
        if 'id="concepts-data"' in html:
            html = re.sub(
                r'<script type="application/json" id="concepts-data">.*?</script>',
                lambda _m: f'<script type="application/json" id="concepts-data">\n{payload}\n  </script>',
                html,
                count=1,
                flags=re.S,
            )
        else:
            html = html.replace(
                "  <script>",
                f'  <script type="application/json" id="concepts-data">\n{payload}\n  </script>\n  <script>',
                1,
            )
        html_path.write_text(html)

    print(f"Wrote {len(all_concepts)} concepts ({len(must)} must-know) → {json_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
