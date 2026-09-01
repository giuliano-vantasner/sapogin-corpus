#!/usr/bin/env python3
"""Cluster source claims into candidate physics paths.

Deterministic TF-IDF + greedy agglomerative clustering over claim statements
(statement_en + tags + quantities). Emits:
  clusters/clusters.json        machine-readable: clusters, members, keywords
  clusters/cluster-report.md    human-readable summary with core-priority flags
  clusters/debt-candidates.md   claims tagged debt-candidate, grouped

This is a PROPOSAL generator: final cluster curation and the campaign split
are human/agent decisions per AGENTS.md ("Clusters are proposals until the
user accepts the campaign split").
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSONL = ROOT / "claims" / "claims.jsonl"
OUTDIR = ROOT / "clusters"

TOKEN = re.compile(r"[a-z0-9][a-z0-9\-]*")
STOP = set(
    """the a an and or of to in on for with by is are was were be been being that this these those
it its as at from into than then so such not no nor but if when while do does did done can could
may might will would shall should must have has had he she they them their his her our your
we you i""".split()
)


def tokens(text: str) -> list[str]:
    return [t for t in TOKEN.findall((text or "").lower()) if t not in STOP and len(t) > 1]


def main() -> int:
    rows = [json.loads(l) for l in JSONL.read_text().splitlines() if l.strip()]
    if not rows:
        print("claims/claims.jsonl is empty — run tools/build_jsonl.py first", file=sys.stderr)
        return 1

    docs = []
    for r in rows:
        parts = [r.get("statement_en") or "", " ".join(r.get("tags") or []),
                 " ".join(r.get("quantities") or []), r.get("doc_title_en") or ""]
        docs.append(tokens(" ".join(parts)))

    df = Counter()
    for toks in docs:
        df.update(set(toks))
    n = len(docs)
    idf = {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}

    vecs = []
    for toks in docs:
        tf = Counter(toks)
        v = {t: (1.0 + math.log(c)) * idf.get(t, 1.0) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})

    def cos(a: dict, b: dict) -> float:
        if len(a) > len(b):
            a, b = b, a
        return sum(x * b.get(t, 0.0) for t, x in a.items())

    THRESHOLD = 0.22
    clusters: list[list[int]] = []
    for i, v in enumerate(vecs):
        best, best_s = None, 0.0
        for ci, members in enumerate(clusters):
            scores = sorted((cos(v, vecs[j]) for j in members), reverse=True)
            mean = sum(scores[: min(5, len(scores))]) / min(5, len(scores))
            if mean > best_s:
                best, best_s = ci, mean
        if best is not None and best_s >= THRESHOLD:
            clusters[best].append(i)
        else:
            clusters.append([i])

    clusters.sort(key=len, reverse=True)
    out_clusters = []
    lines = ["# Cluster report (PROPOSAL — requires user-accepted campaign split)", ""]
    for ci, members in enumerate(clusters, 1):
        kw = Counter()
        for j in members:
            kw.update(vecs[j])
        keywords = [t for t, _ in kw.most_common(12)]
        ids = [rows[j]["id"] for j in members]
        core = [rows[j]["id"] for j in members if rows[j].get("priority") == "core"]
        secs = sorted({rows[j].get("section") or "?" for j in members})
        facets = sorted({rows[j].get("facet") or "?" for j in members})
        out_clusters.append(
            {"cluster": ci, "size": len(members), "keywords": keywords,
             "claim_ids": ids, "core_ids": core, "sections": secs, "facets": facets}
        )
        lines += [
            f"## Cluster {ci} — {len(members)} claims — keywords: {', '.join(keywords[:8])}",
            f"- sections: {', '.join(secs)}; facets: {', '.join(facets)}",
            f"- core-priority claims: {len(core)}"
            + (f" ({', '.join(core[:8])}{' …' if len(core) > 8 else ''})" if core else ""),
            f"- claims: {', '.join(ids[:12])}{' …' if len(ids) > 12 else ''}",
            "",
        ]

    debt = defaultdict(list)
    for r in rows:
        if "debt-candidate" in (r.get("tags") or []):
            debt[r.get("doc_id") or "?"].append(r["id"])
    debt_lines = ["# Debt candidates (claims whose content conflicts with accepted physics", "",
                  "# per extractor tagging — clustering phase promotes these to governance/debt.yaml)", ""]
    for did, ids in sorted(debt.items()):
        debt_lines.append(f"- {did}: {', '.join(ids)}")
    if not debt:
        debt_lines.append("- none tagged yet")

    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / "clusters.json").write_text(json.dumps(out_clusters, ensure_ascii=False, indent=1))
    (OUTDIR / "cluster-report.md").write_text("\n".join(lines))
    (OUTDIR / "debt-candidates.md").write_text("\n".join(debt_lines) + "\n")
    sizes = ", ".join(str(c["size"]) for c in out_clusters)
    print(f"{len(out_clusters)} clusters (sizes {sizes}); debt candidates: "
          f"{sum(len(v) for v in debt.values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
