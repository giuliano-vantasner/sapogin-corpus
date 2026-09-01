#!/usr/bin/env python3
"""Static file server + JSON API for the sapogin-corpus explorer.

Serves web/ at / and an agent-facing API under /api:
  /api/search?q=TERM[&bucket=&priority=&facet=&doc=&limit=]
  /api/claim/SC-AR04-005          full claim record (+cluster/bucket)
  /api/clusters                   all clusters (id, bucket, size, keywords, core)
  /api/cluster/<cluster-id>       cluster meta + member claim ids
  /api/buckets                    bucket summary
  /api/synthesis/<bucket>         raw markdown synthesis
  /api/random?n=5[&bucket=]       n random claims (exploration)
  /api/stats                      corpus overview
Deterministic ranking; loads claims/clusters/synthesis into memory at start.
"""
import json
import math
import random
import re
import sys
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"

TOKEN = re.compile(r"[a-z\u0400-\u04ff0-9][a-z\u0400-\u04ff0-9\-]*", re.IGNORECASE)
STOP = set("""the a an and or of to in on for with by is are was were be been being that
this these those it its as at from into than then so such not no nor but if when while
do does did done can could may might will would shall should must have has had""".split())

claims, clusters, bucket_of, synthesis, docs = [], {}, {}, {}, {}


def tok(text):
    return [t for t in TOKEN.findall((text or "").lower()) if t not in STOP and len(t) > 1]


def load():
    global claims, clusters, synthesis, bucket_of, DF, N, docs
    rows = [json.loads(l) for l in (ROOT / "claims" / "claims.jsonl").read_text().splitlines() if l.strip()]
    clusters = json.loads((ROOT / "clusters" / "clusters.json").read_text())
    claim_cluster = {cid: c["cluster"] for c in clusters for cid in c["claim_ids"]}
    bucket_of = {c["cluster"]: c["bucket"] for c in clusters}
    manifest = yaml.safe_load((ROOT / "papers" / "MANIFEST.yaml").read_text())
    docs = {d["doc_id"]: d for d in manifest["documents"]}
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
    sdir = ROOT / "synthesis"
    if sdir.is_dir():
        synthesis = {m.stem: m.read_text() for m in sorted(sdir.glob("*.md"))}
    DF = Counter()
    N = len(claims)
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


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _static(self, path):
        if path == "/":
            path = "/index.html"
        f = (WEB / path.lstrip("/")).resolve()
        if not str(f).startswith(str(WEB.resolve())) or not f.is_file():
            self._json({"error": "not found"}, 404)
            return
        # allow the papers symlink
        try:
            f.relative_to(WEB.resolve())
        except ValueError:
            pass
        ctype = {".html": "text/html", ".js": "text/javascript", ".css": "text/css",
                 ".json": "application/json", ".md": "text/markdown", ".yaml": "text/yaml"}.get(
                     f.suffix, "application/octet-stream")
        body = f.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        try:
            self.route()
        except Exception as e:  # noqa: BLE001
            self._json({"error": str(e)}, 500)

    @staticmethod
    def _utf8(s):
        # http.server decodes the request line as latin-1; recover UTF-8
        try:
            return s.encode("iso-8859-1").decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            return s

    def route(self):
        path, _, qs = self.path.partition("?")
        path = self._utf8(path)
        q = {k: self._utf8(v) for k, v in
             (kv.split("=", 1) for kv in qs.split("&") if "=" in kv)}
        path = path.rstrip("/") or "/"

        if not path.startswith("/api"):
            return self._static(path)

        if path == "/api/search":
            terms = tok(q.get("q", ""))
            hits = claims
            for k in ("bucket", "priority", "facet", "doc", "section", "cluster"):
                if q.get(k):
                    hits = [c for c in hits if c.get(k) == q[k]]
            if terms:
                scored = [(score(c, terms), c) for c in hits]
                hits = [c for s, c in sorted(scored, key=lambda x: -x[0]) if s > 0]
            lim = min(int(q.get("limit", "20")), 100)
            return self._json({"query": q.get("q", ""), "total": len(hits),
                               "results": hits[:lim]})

        if path.startswith("/api/claim/"):
            cid = path.rsplit("/", 1)[-1].upper()
            for c in claims:
                if c["id"] == cid:
                    return self._json(c)
            return self._json({"error": f"unknown claim id {cid}"}, 404)

        if path == "/api/clusters":
            return self._json([{"cluster": c["cluster"], "bucket": c["bucket"],
                                "size": c["size"], "core": len(c["core_ids"]),
                                "keywords": c["keywords"]} for c in clusters])

        if path.startswith("/api/cluster/"):
            cid = path.rsplit("/", 1)[-1]
            for c in clusters:
                if c["cluster"] == cid:
                    return self._json({**{k: c[k] for k in ("cluster", "bucket", "size", "keywords")},
                                       "core_ids": c["core_ids"], "claim_ids": c["claim_ids"],
                                       "synthesis": bool(c["bucket"] in synthesis)})
            return self._json({"error": f"unknown cluster {cid}"}, 404)

        if path == "/api/buckets":
            out = {}
            for c in clusters:
                b = out.setdefault(c["bucket"], {"bucket": c["bucket"], "clusters": 0, "claims": 0})
                b["clusters"] += 1
                b["claims"] += c["size"]
            return self._json(sorted(out.values(), key=lambda b: -b["claims"]))

        if path.startswith("/api/synthesis/"):
            b = path.rsplit("/", 1)[-1]
            if b in synthesis:
                return self._json({"bucket": b, "markdown": synthesis[b]})
            return self._json({"error": f"no synthesis for {b}", "available": sorted(synthesis)}, 404)

        if path == "/api/random":
            pool = claims
            if q.get("bucket"):
                pool = [c for c in pool if c["bucket"] == q["bucket"]]
            n = min(int(q.get("n", "5")), 50)
            return self._json(random.sample(pool, min(n, len(pool))))

        if path == "/api/stats":
            return self._json({
                "claims": len(claims), "documents": len(docs),
                "clusters": len(clusters), "buckets": len(set(bucket_of.values())),
                "syntheses": sorted(synthesis),
                "core": sum(1 for c in claims if c["priority"] == "core"),
                "endpoints": ["/api/search?q=", "/api/claim/<id>", "/api/clusters",
                              "/api/cluster/<id>", "/api/buckets", "/api/synthesis/<bucket>",
                              "/api/random?n=", "/api/stats"]})

        self._json({"error": "unknown endpoint", "try": "/api/stats"}, 404)

    def log_message(self, *a):  # quiet
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8420
    load()
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"sapogin-corpus explorer + API on http://127.0.0.1:{port} "
          f"({N} claims, {len(clusters)} clusters, {len(synthesis)} syntheses)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
