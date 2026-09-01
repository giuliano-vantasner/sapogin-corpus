#!/usr/bin/env python3
"""Ingest claims/claims.jsonl as Claim nodes into the GitNexus graph.

Attempts raw Cypher CREATE through `gitnexus cypher`. If the CLI rejects
writes, emits a loadable Cypher script at clusters/claims-ingest.cypher and
prints the manual path instead. Idempotent per claim ID (MERGE semantics).
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSONL = ROOT / "claims" / "claims.jsonl"
OUT = ROOT / "clusters" / "claims-ingest.cypher"


def cypher_escape(s: str) -> str:
    if s is None:
        return "''"
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"


def main() -> int:
    rows = [json.loads(l) for l in JSONL.read_text().splitlines() if l.strip()]
    stmts = []
    for r in rows:
        props = ", ".join(
            f"{k}: {cypher_escape(v)}"
            for k, v in (
                ("id", r["id"]), ("doc_id", r.get("doc_id")), ("section", r.get("section")),
                ("type", r.get("type")), ("facet", r.get("facet")), ("priority", r.get("priority")),
                ("statement_en", r.get("statement_en")), ("quote_ru", r.get("quote_ru")),
                ("file", r.get("file")), ("page", r.get("page")),
            )
        )
        stmts.append(f"MERGE (c:Claim {{id: {cypher_escape(r['id'])}}}) SET {props};")
        for rel in r.get("relations") or []:
            if rel.get("to"):
                kind = cypher_escape(rel.get("kind", "relates"))
                stmts.append(
                    f"MATCH (a:Claim {{id: {cypher_escape(r['id'])}}}), "
                    f"(b:Claim {{id: {cypher_escape(rel['to'])}}}) "
                    f"MERGE (a)-[:{kind.upper()}]->(b);"
                )
    script = "\n".join(stmts) + "\n"
    OUT.write_text(script)
    applied = 0
    for stmt in stmts:
        r = subprocess.run(["gitnexus", "cypher", stmt], capture_output=True, text=True, cwd=ROOT)
        if r.returncode == 0:
            applied += 1
        else:
            first_err = (r.stderr or r.stdout).strip().splitlines()[:1]
            print(f"write rejected by gitnexus at stmt {applied}: {first_err}", file=sys.stderr)
            print(f"manual path: {OUT.relative_to(ROOT)} ({len(stmts)} statements)", file=sys.stderr)
            return 2
    print(f"ingested {len(rows)} Claim nodes, {len(stmts)} statements applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
