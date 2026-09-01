"""Corpus state, loading, ranking, and shared query functions.

Every in-memory corpus value lives here. HTTP and MCP adapters call the same
query helpers so their search, claim, cluster, document, and stats semantics
cannot drift.
"""
import json
import math
import random
import re
from collections import Counter
from pathlib import Path

import yaml

from corpus_common import cluster_summary, cluster_title

ROOT = Path(__file__).resolve().parent.parent.parent
WEB = ROOT / "web"

TOKEN = re.compile(r"[a-z\u0400-\u04ff0-9][a-z\u0400-\u04ff0-9\-]*", re.IGNORECASE)
STOP = set("""the a an and or of to in on for with by is are was were be been being that
this these those it its as at from into than then so such not no nor but if when while
do does did done can could may might will would shall should must have has had""".split())

claims, clusters, bucket_of, synthesis, docs = [], [], {}, {}, {}


def tok(text):
    return [t for t in TOKEN.findall((text or "").lower()) if t not in STOP and len(t) > 1]


def load():
    global claims, clusters, synthesis, bucket_of, DF, N, docs, N_doc_sources
    claims.clear()
    rows = [json.loads(l) for l in (ROOT / "claims" / "claims.jsonl").read_text().splitlines() if l.strip()]
    clusters.clear()
    clusters.extend(json.loads((ROOT / "clusters" / "clusters.json").read_text()))
    claim_cluster = {cid: c["cluster"] for c in clusters for cid in c["claim_ids"]}
    bucket_of.clear()
    bucket_of.update({c["cluster"]: c["bucket"] for c in clusters})
    manifest = yaml.safe_load((ROOT / "papers" / "MANIFEST.yaml").read_text())
    docs.clear()
    docs.update({d["doc_id"]: d for d in manifest["documents"]})
    for i, page in enumerate(["home", "articles", "brochure", "dissertation",
                              "lectures", "monography", "patents",
                              "perpetual_motion", "teaching", "technologies",
                              "works"], 1):
        docs[f"SI{i:02d}"] = {"doc_id": f"SI{i:02d}", "section": "site",
                              "title_ru": f"sapogin.com /{page}",
                              "file": f"site/{page}.md"}
    for r in rows:
        d = docs.get(r["doc_id"], {})
        cl = claim_cluster.get(r["id"])
        claims.append({
            "id": r["id"], "cluster": cl, "bucket": bucket_of.get(cl),
            "doc": r["doc_id"], "title": r.get("doc_title_en") or "",
            "section": d.get("section", "?"), "pdf": d.get("file", ""),
            "type": r.get("type"), "facet": r.get("facet"), "priority": r.get("priority"),
            "page": r.get("page"), "statement": r.get("statement_en") or "",
            "quote": r.get("quote_ru") or "", "tags": r.get("tags") or [],
            "quantities": r.get("quantities") or [], "materials": r.get("materials") or [],
            "geometry": r.get("geometry") or [], "steps": r.get("procedure_steps") or [],
            "measurements": r.get("measurements") or [], "schematic_refs": r.get("schematic_refs") or [],
        })
    statement_of = {c["id"]: c["statement"] for c in claims}
    for c in clusters:
        c["title"] = cluster_title(c["keywords"])
        c["summary"] = cluster_summary(c, statement_of)
    sdir = ROOT / "synthesis"
    if sdir.is_dir():
        synthesis.clear()
        synthesis.update({m.stem: m.read_text() for m in sorted(sdir.glob("*.md"))})
    DF = Counter()
    N = len(claims)
    N_doc_sources = len(docs)
    for c in claims:
        DF.update(set(tok(" ".join([c["statement"], c["quote"], " ".join(c["tags"]), c["id"]]))))


def score(c, terms):
    blob_s, blob_q = tok(c["statement"]), tok(c["quote"])
    tags = [t.lower() for t in c["tags"]]
    s = 0.0
    for t in terms:
        idf = math.log((N + 1) / (DF.get(t, 0) + 1)) + 1.0
        s += 2.0 * idf * blob_s.count(t)
        s += 1.0 * idf * blob_q.count(t)
        if any(t in tg for tg in tags):
            s += 3.0 * idf
        if t in c["id"].lower():
            s += 25.0
    return s


# ---- query helpers: the single source of truth for API + MCP ----

FILTER_KEYS = ("bucket", "priority", "facet", "doc", "section", "cluster")


def has_query(params):
    return bool(tok(params.get("q", "")) or any(params.get(k) for k in FILTER_KEYS))


def search(params):
    """Filter and rank claims; callers own transport-specific pagination/errors."""
    terms = tok(params.get("q", ""))
    hits = claims
    for key in FILTER_KEYS:
        if params.get(key):
            hits = [claim for claim in hits if claim.get(key) == params[key]]
    if terms:
        scored = [(score(claim, terms), claim) for claim in hits]
        hits = [claim for rank, claim in sorted(scored, key=lambda item: -item[0])
                if rank > 0]
    return hits


def search_page(params, default_limit):
    hits = search(params)
    limit = min(int(params.get("limit", default_limit)), 100)
    offset = max(int(params.get("offset", 0)), 0)
    return {"total": len(hits), "offset": offset,
            "next_offset": offset + limit if offset + limit < len(hits) else None,
            "results": hits[offset:offset + limit]}


def claim_by_id(claim_id):
    return next((claim for claim in claims if claim["id"] == claim_id), None)


def cluster_by_id(cluster_id):
    return next((cluster for cluster in clusters
                 if cluster["cluster"] == cluster_id), None)


def clusters_list(bucket=None):
    selected = [cluster for cluster in clusters
                if not bucket or cluster["bucket"] == bucket]
    return [cluster_payload(cluster, detail=False) for cluster in selected]


def cluster_detail(cluster_id):
    cluster = cluster_by_id(cluster_id)
    return cluster_payload(cluster) if cluster is not None else None


def buckets_summary():
    out = {}
    for cluster in clusters:
        bucket = out.setdefault(
            cluster["bucket"],
            {"bucket": cluster["bucket"], "clusters": 0, "claims": 0},
        )
        bucket["clusters"] += 1
        bucket["claims"] += cluster["size"]
    return sorted(out.values(), key=lambda bucket: -bucket["claims"])


def synthesis_of(bucket):
    return synthesis.get(bucket)


def random_sample(count, bucket=None):
    pool = claims if not bucket else [
        claim for claim in claims if claim["bucket"] == bucket
    ]
    return random.sample(pool, min(count, len(pool)))


def cluster_payload(c, detail=True):
    out = {"cluster": c["cluster"], "bucket": c["bucket"], "size": c["size"],
           "title": c.get("title", ""), "summary": c.get("summary", ""),
           "keywords": c["keywords"], "facets": c.get("facets", []),
           "core": len(c["core_ids"])}
    if detail:
        out.update({"core_ids": c["core_ids"], "claim_ids": c["claim_ids"],
                    "synthesis": bool(c["bucket"] in synthesis)})
    return out


def docs_payload():
    per = Counter(c["doc"] for c in claims)
    core_per = Counter(c["doc"] for c in claims if c["priority"] == "core")
    title_en = {}
    for c in claims:
        if c["doc"] not in title_en and c.get("title"):
            title_en[c["doc"]] = c["title"]
    out = []
    for d in sorted(docs.values(), key=lambda d: d["doc_id"]):
        entry = {"doc_id": d["doc_id"],
                 "kind": "site" if d.get("section") == "site" else "paper",
                 "section": d.get("section", "?"),
                 "title": title_en.get(d["doc_id"]) or d.get("title_ru", ""),
                 "path": "/" + d["file"],
                 "claims": per.get(d["doc_id"], 0),
                 "core": core_per.get(d["doc_id"], 0)}
        if d.get("bytes"):
            entry["bytes"] = d["bytes"]
        out.append(entry)
    return {"documents": out, "total": len(out)}


def stats_payload(base: str) -> dict:
    n_site = sum(1 for d in docs.values() if d.get("section") == "site")
    return {"claims": N, "sources": N_doc_sources, "papers": N_doc_sources - n_site,
            "site_pages": n_site, "clusters": len(clusters),
            "buckets": sorted(set(bucket_of.values())),
            "core": sum(1 for c in claims if c["priority"] == "core"),
            "syntheses": sorted(synthesis),
            "mcp": base + "/mcp",
            "api": [base + e for e in
                    ["/api/search?q=", "/api/claim/<id>", "/claim/<id>",
                     "/api/clusters", "/api/cluster/<id>", "/api/buckets",
                     "/api/synthesis/<bucket>", "/api/docs", "/api/random?n=",
                     "/api/export.jsonl", "/api/stats"]]}
