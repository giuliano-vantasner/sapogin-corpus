#!/usr/bin/env python3
"""Cluster source claims into candidate physics paths.

Two-stage deterministic clustering:
  1. Bucket by curated topic family (tags + statement keywords, ordered rules
     aligned with governance/policy.yaml core topics and the Sapogin topic
     map) — first matching rule wins.
  2. Within each bucket: TF-IDF + greedy agglomerative (mean-of-top-5 cosine),
     per-bucket idf. CLUSTER_THRESHOLD env overrides the 0.22 default.

Emits:
  clusters/clusters.json        machine-readable: clusters, members, keywords
  clusters/cluster-report.md    human-readable summary with core-priority flags
  clusters/debt-candidates.md   claims tagged debt-candidate, grouped

This is a PROPOSAL generator: final cluster curation and the campaign split
are human/agent decisions per AGENTS.md ("Clusters are proposals until the
user accepts the campaign split").
"""
import json
import math
import os
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

# Ordered topic-family rules: (bucket, substrings). FIRST match wins, so the
# most specific families come first. Aligned with policy.yaml core topics
# (transmutation, catalysis, EVO, electrical path) and the Sapogin topic map.
BUCKETS: list[tuple[str, tuple[str, ...]]] = [
    ("transmutation-nuclear", (
        "transmut", "изотоп", "ядерн", "протонн", "nucleus", "nuclear",
        "isotop", "протонные зарядовые", "нейтрон")),
    ("catalysis", ("catalys", "катализ", "каталит")),
    ("evo-charge-clusters", (
        "кластер", "cluster", "evo", "shoulders", "шоулдерс",
        "зарядов", "charge cluster")),
    ("electrical-devices", (
        "варикап", "varicap", "диод", "diode", "устройств", "установк",
        "инжектор", "injector", "testatika", "тестатика", "конденсатор",
        "capacitor", "генератор", "generator", "электрометр", "electrometer",
        "квантовый", "energy converter", "преобразовател", "контур",
        "circuit", "колеба", "oscillat", "эдс", "emf", "термоэлектрон",
        "thermoelectron", "модуляц", "modulat", "нестабильн", "instabilit")),
    ("discharge-plasma", (
        "разряд", "discharge", "плазм", "plasma", "взрыв", "explos",
        "skin", "поверхностн", "плотность тока", "current densit",
        "провод", "wire", "molten", "оплавлен")),
    ("emden-gravity-cosmic", (
        "emden", "эмден", "гравит", "gravit", "черн", "black hole",
        "звезд", "star", "тунгуск", "tunguska", "космолог", "cosmolog",
        "планет", "planet", "enceladus", "энцелад")),
    ("foundations-canonical", (
        "canonical", "каноническ", "биволн", "biwave", "наименьшего действия",
        "least action", "лагранж", "lagrang", "волнов", "wave")),
]
FALLBACK_BUCKET = "general"


def tokens(text: str) -> list[str]:
    return [t for t in TOKEN.findall((text or "").lower()) if t not in STOP and len(t) > 1]


def bucket_of(r: dict) -> str:
    blob = " ".join([r.get("statement_en") or "", " ".join(r.get("tags") or []),
                     r.get("doc_title_en") or "", r.get("doc_title_ru") or ""]).lower()
    for name, subs in BUCKETS:
        if any(s in blob for s in subs):
            return name
    return FALLBACK_BUCKET


def greedy_cluster(vecs: list[dict], threshold: float) -> list[list[int]]:
    clusters: list[list[int]] = []
    for i, v in enumerate(vecs):
        best, best_s = None, 0.0
        for ci, members in enumerate(clusters):
            scores = sorted((sum(x * vecs[j].get(t, 0.0) for t, x in v.items())
                             for j in members), reverse=True)
            mean = sum(scores[: min(5, len(scores))]) / min(5, len(scores))
            if mean > best_s:
                best, best_s = ci, mean
        if best is not None and best_s >= threshold:
            clusters[best].append(i)
        else:
            clusters.append([i])
    return clusters


def main() -> int:
    rows = [json.loads(l) for l in JSONL.read_text().splitlines() if l.strip()]
    if not rows:
        print("claims/claims.jsonl is empty — run tools/build_jsonl.py first", file=sys.stderr)
        return 1

    threshold = float(os.environ.get("CLUSTER_THRESHOLD", "0.10"))

    by_bucket: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        by_bucket[bucket_of(r)].append(i)

    out_clusters = []
    lines = ["# Cluster report (PROPOSAL — requires user-accepted campaign split)", ""]
    for bucket, idxs in sorted(by_bucket.items(), key=lambda kv: -len(kv[1])):
        docs = []
        for i in idxs:
            r = rows[i]
            toks = tokens(" ".join([
                r.get("statement_en") or "",
                " ".join(r.get("tags") or []),
                " ".join(r.get("quantities") or []),
                r.get("doc_title_en") or ""]))
            docs.append(toks)
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
        groups = greedy_cluster(vecs, threshold) if n > 2 else [list(range(n))]

        lines.append(f"## {bucket} — {len(idxs)} claims, {len(groups)} clusters")
        lines.append("")
        for gi, members in enumerate(groups, 1):
            kw = Counter()
            for j in members:
                kw.update(vecs[j])
            keywords = [t for t, _ in kw.most_common(12)]
            ids = [rows[idxs[j]]["id"] for j in members]
            core = [rows[idxs[j]]["id"] for j in members if rows[idxs[j]].get("priority") == "core"]
            secs = sorted({rows[idxs[j]].get("section") or "?" for j in members})
            facets = sorted({rows[idxs[j]].get("facet") or "?" for j in members})
            out_clusters.append(
                {"cluster": f"{bucket}-{gi:02d}", "bucket": bucket, "size": len(members),
                 "keywords": keywords, "claim_ids": ids, "core_ids": core,
                 "sections": secs, "facets": facets})
            lines += [
                f"### {bucket}-{gi:02d} — {len(members)} claims — keywords: {', '.join(keywords[:8])}",
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
    print(f"{len(out_clusters)} clusters in {len(by_bucket)} buckets (sizes {sizes}); "
          f"debt candidates: {sum(len(v) for v in debt.values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
