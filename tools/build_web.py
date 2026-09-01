#!/usr/bin/env python3
"""Build web/data.js for the local claim/cluster explorer.

Inputs: claims/claims.jsonl, clusters/clusters.json, papers/MANIFEST.yaml,
synthesis/*.md (optional). Output: web/data.js (window.SAPOGIN).
Deterministic; rerun after any claims/clusters/synthesis change.
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    rows = [json.loads(l) for l in (ROOT / "claims" / "claims.jsonl").read_text().splitlines() if l.strip()]
    clusters = json.loads((ROOT / "clusters" / "clusters.json").read_text())

    claim_cluster: dict[str, str] = {}
    for c in clusters:
        for cid in c["claim_ids"]:
            claim_cluster[cid] = c["cluster"]

    manifest = yaml.safe_load((ROOT / "papers" / "MANIFEST.yaml").read_text())
    docs = {}
    for d in manifest["documents"]:
        docs[d["doc_id"]] = {
            "doc_id": d["doc_id"], "section": d["section"],
            "title_ru": d.get("title_ru") or "", "pdf": d["file"],
        }

    claims, edges = [], []
    for r in rows:
        doc = docs.get(r["doc_id"], {})
        claims.append({
            "id": r["id"], "cluster": claim_cluster.get(r["id"], "?"),
            "doc": r["doc_id"], "title": r.get("doc_title_en") or doc.get("title_ru") or "",
            "section": r.get("section") or doc.get("section") or "?",
            "facet": r.get("facet") or "?", "type": r.get("type") or "?",
            "priority": r.get("priority") or "?", "page": r.get("page"),
            "pdf": doc.get("pdf") or "",
            "statement": r.get("statement_en") or "", "quote": r.get("quote_ru") or "",
            "tags": r.get("tags") or [], "quantities": r.get("quantities") or [],
            "materials": r.get("materials") or [], "geometry": r.get("geometry") or [],
            "steps": r.get("procedure_steps") or [], "meas": r.get("measurements") or [],
            "schematics": r.get("schematic_refs") or [],
        })
        for rel in (r.get("relations") or []):
            if isinstance(rel, dict) and rel.get("to"):
                edges.append({"from": r["id"], "to": rel["to"],
                              "kind": rel.get("kind") or "related"})

    bucket_of = {c["cluster"]: c["bucket"] for c in clusters}
    buckets = {}
    for c in clusters:
        b = buckets.setdefault(c["bucket"], {"name": c["bucket"], "size": 0, "clusters": 0})
        b["size"] += c["size"]
        b["clusters"] += 1

    synthesis = {}
    sdir = ROOT / "synthesis"
    if sdir.is_dir():
        for md in sorted(sdir.glob("*.md")):
            synthesis[md.stem] = md.read_text()

    out = {
        "generated": "see git log", "buckets": sorted(buckets.values(), key=lambda b: -b["size"]),
        "clusters": [{"id": c["cluster"], "bucket": c["bucket"], "size": c["size"],
                      "keywords": c["keywords"], "core": len(c["core_ids"])} for c in clusters],
        "claims": claims, "edges": edges, "synthesis": synthesis,
    }
    dest = ROOT / "web" / "data.js"
    dest.write_text("window.SAPOGIN = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")
    n_syn = len(synthesis)
    print(f"web/data.js: {len(claims)} claims, {len(clusters)} clusters, {len(edges)} edges, {n_syn} syntheses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
