#!/usr/bin/env python3
"""Flatten claims/source/*.yaml into claims/claims.jsonl for GitNexus ingestion."""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "claims" / "claims.jsonl"


def main() -> int:
    rows = []
    for cf in sorted((ROOT / "claims" / "source").glob("*.yaml")):
        data = yaml.safe_load(cf.read_text()) or {}
        doc = data.get("document", {})
        for c in data.get("claims") or []:
            rows.append(
                {
                    "id": c["id"],
                    "doc_id": doc.get("doc_id"),
                    "section": doc.get("section"),
                    "doc_title_en": doc.get("title_en"),
                    "doc_title_ru": doc.get("title_ru"),
                    "file": doc.get("file"),
                    "md5": doc.get("md5"),
                    "type": c.get("type"),
                    "facet": c.get("facet"),
                    "priority": c.get("priority"),
                    "page": c.get("page"),
                    "statement_en": c.get("statement_en"),
                    "quote_ru": c.get("quote_ru"),
                    "quantities": c.get("quantities") or [],
                    "equations": c.get("equations") or [],
                    "materials": c.get("materials") or [],
                    "geometry": c.get("geometry") or [],
                    "procedure_steps": c.get("procedure_steps") or [],
                    "measurements": c.get("measurements") or [],
                    "schematic_refs": c.get("schematic_refs") or [],
                    "tags": c.get("tags") or [],
                    "relations": c.get("relations") or [],
                }
            )
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} claims to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
