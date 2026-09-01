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
        self.send_header("Link", '</mcp>; rel="mcp-server"')
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

    def do_POST(self):
        if self.path.rstrip("/") == "/mcp":
            try:
                self.mcp_endpoint()
            except Exception as e:  # noqa: BLE001
                self._json({"jsonrpc": "2.0", "id": None,
                            "error": {"code": -32603, "message": str(e)}}, 500)
            return
        self.send_response(405)
        self.send_header("Allow", "GET")
        self.end_headers()

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

        if path == "/mcp":
            return self.mcp_endpoint()

        if path == "/llms.txt":
            body = LLMSTXT.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/robots.txt":
            body = ROBOTS.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/.well-known/ai-plugin.json" or path == "/.well-known/mcp":
            return self._json({
                "schema_version": "v1",
                "name_for_human": "Sapogin Corpus Explorer",
                "name_for_model": "sapogin-corpus",
                "description_for_human": "Explore 1,641 extracted claims from Sapogin's 'Canonical Physics' corpus: search, clusters, syntheses.",
                "description_for_model": "Search and explore the sapogin-corpus: 1,641 provenance-pinned source claims (LENR/EVO research) in 145 clusters / 8 buckets, with practical-first syntheses. Use /api/search (q, bucket, priority, facet, limit), /api/claim/<id>, /api/cluster/<id>, /api/synthesis/<bucket>, /api/stats. MCP streamable-HTTP server at /mcp (no auth).",
                "api": {"type": "openapi", "url": "/openapi.json"},
                "auth": {"type": "none"},
            })

        if path == "/openapi.json":
            return self._json(OPENAPI)

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

    # ---- MCP streamable HTTP (stateless, open) ----
    def mcp_endpoint(self):
        if self.command != "POST":
            self.send_response(405)
            self.send_header("Allow", "POST")
            self.end_headers()
            return
        n = int(self.headers.get("Content-Length") or 0)
        try:
            msg = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return self._json({"jsonrpc": "2.0", "id": None,
                               "error": {"code": -32700, "message": "Parse error"}}, 400)
        resp = mcp_dispatch(msg)
        if resp is None:  # notification
            self.send_response(202)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self._json(resp)

    def log_message(self, *a):  # quiet
        pass



# ---- MCP server: tools over streamable HTTP, no auth ----
PROTOCOL_VERSION = "2025-06-18"

MCP_TOOLS = [
    {"name": "search_claims",
     "description": "Full-text search over 1,641 provenance-pinned Sapogin 'Canonical Physics' claims (English statements, Russian quotes, tags, SC-* ids). Filters: bucket, priority (core|normal), facet (theory|phenomenology|experiment|measurement|recipe|material|process|procedure|schematic|geometry), doc, section, cluster.",
     "inputSchema": {"type": "object", "properties": {
         "q": {"type": "string"}, "bucket": {"type": "string"},
         "priority": {"type": "string"}, "facet": {"type": "string"},
         "doc": {"type": "string"}, "section": {"type": "string"},
         "cluster": {"type": "string"},
         "limit": {"type": "integer", "default": 15}},
         "required": ["q"]}},
    {"name": "get_claim",
     "description": "Full record of one claim by SC-* id: statement, verbatim quote_ru, quantities, materials, geometry, procedure_steps, measurements, schematic_refs, source pdf path+page.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "list_clusters",
     "description": "List all 145 proposal clusters (id, bucket, size, core count, keywords).",
     "inputSchema": {"type": "object", "properties": {"bucket": {"type": "string"}}}},
    {"name": "get_cluster",
     "description": "One cluster's meta, keywords, and member claim ids.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "get_synthesis",
     "description": "Practical-first synthesis markdown for a bucket (the art before the theory).",
     "inputSchema": {"type": "object", "properties": {"bucket": {"type": "string"}}, "required": ["bucket"]}},
    {"name": "corpus_stats",
     "description": "Corpus overview: counts, buckets, syntheses, endpoint list.",
     "inputSchema": {"type": "object", "properties": {}}},
]


def _tool_search(a):
    terms = tok(a.get("q", ""))
    hits = claims
    for k in ("bucket", "priority", "facet", "doc", "section", "cluster"):
        if a.get(k):
            hits = [c for c in hits if c.get(k) == a[k]]
    if terms:
        scored = [(score(c, terms), c) for c in hits]
        hits = [c for s, c in sorted(scored, key=lambda x: -x[0]) if s > 0]
    return {"total": len(hits),
            "results": hits[:min(int(a.get("limit", 15)), 100)]}


def _tool_claim(a):
    cid = str(a.get("id", "")).upper()
    for c in claims:
        if c["id"] == cid:
            return c
    return {"error": f"unknown claim id {cid}"}


def _tool_clusters(a):
    sel = [c for c in clusters if not a.get("bucket") or c["bucket"] == a["bucket"]]
    return [{"cluster": c["cluster"], "bucket": c["bucket"], "size": c["size"],
             "core": len(c["core_ids"]), "keywords": c["keywords"]} for c in sel]


def _tool_cluster(a):
    for c in clusters:
        if c["cluster"] == a.get("id"):
            return {**{k: c[k] for k in ("cluster", "bucket", "size", "keywords")},
                    "core_ids": c["core_ids"], "claim_ids": c["claim_ids"],
                    "synthesis": c["bucket"] in synthesis}
    return {"error": f"unknown cluster {a.get('id')}"}


def _tool_synthesis(a):
    b = a.get("bucket", "")
    return {"bucket": b, "markdown": synthesis[b]} if b in synthesis else {
        "error": f"no synthesis for {b}", "available": sorted(synthesis)}


def _tool_stats(a):
    return {"claims": N, "documents": len(docs), "clusters": len(clusters),
            "buckets": sorted(set(bucket_of.values())),
            "core": sum(1 for c in claims if c["priority"] == "core"),
            "syntheses": sorted(synthesis),
            "api": ["/api/search?q=", "/api/claim/<id>", "/api/clusters",
                    "/api/cluster/<id>", "/api/buckets", "/api/synthesis/<bucket>",
                    "/api/random?n=", "/api/stats"]}


MCP_DISPATCH = {
    "search_claims": _tool_search, "get_claim": _tool_claim,
    "list_clusters": _tool_clusters, "get_cluster": _tool_cluster,
    "get_synthesis": _tool_synthesis, "corpus_stats": _tool_stats,
}


def mcp_dispatch(msg):
    method = msg.get("method", "")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": msg.get("params", {}).get("protocolVersion", PROTOCOL_VERSION),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "sapogin-corpus", "version": "1.0.0",
                           "description": "1,641 provenance-pinned claims from Sapogin's 'Canonical Physics' (LENR/EVO corpus) with clusters and syntheses"}}}
    if method.startswith("notifications/"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": MCP_TOOLS}}
    if method == "tools/call":
        name = msg.get("params", {}).get("name", "")
        args = msg.get("params", {}).get("arguments", {}) or {}
        fn = MCP_DISPATCH.get(name)
        if not fn:
            return {"jsonrpc": "2.0", "id": mid, "result": {
                "isError": True,
                "content": [{"type": "text", "text": f"unknown tool {name}"}]}}
        try:
            payload = fn(args)
        except Exception as e:  # noqa: BLE001
            payload = {"error": str(e)}
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=1)}]}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"Method not found: {method}"}}


LLMSTXT = """# sapogin-corpus

> 1,641 provenance-pinned source claims extracted from Vladimir Sapogin's
> "Canonical Physics" site and 54 papers (LENR / EVO / charge-cluster research),
> organized into 145 proposal clusters across 8 topic buckets, with
> practical-first syntheses. Data, not doctrine: every claim carries a verbatim
> Russian quote, English translation, and source-PDF page reference.

Agents can explore three ways, all open (no auth):

1. MCP (preferred): streamable-HTTP server at /mcp — tools: search_claims,
   get_claim, list_clusters, get_cluster, get_synthesis, corpus_stats.
   Point any MCP client at http://127.0.0.1:8420/mcp (POST, JSON-RPC 2.0).
2. JSON API: /api/search?q= (filters: bucket, priority, facet, doc, section,
   cluster, limit), /api/claim/<SC-ID>, /api/clusters, /api/cluster/<id>,
   /api/buckets, /api/synthesis/<bucket>, /api/random?n=, /api/stats.
   Machine-readable spec: /openapi.json
3. Human UI: / (graph + browse + search; agents may also read web/data.js).

Key buckets: transmutation-nuclear, catalysis, evo-charge-clusters,
electrical-devices, discharge-plasma, emden-gravity-cosmic,
foundations-canonical, general. Priority "core" = transmutation / catalysis /
EVO / electrical path.

Practical layer first: recipes, materials, geometry, procedures, measurements.
Source PDFs under /papers/<section>/<file>.pdf (paths returned by the API).
"""

ROBOTS = """User-agent: *
Allow: /

# Agents: MCP streamable-HTTP server at /mcp (JSON-RPC 2.0, no auth)
# JSON API: /api/search?q= ... see /llms.txt and /openapi.json
"""

OPENAPI = {
    "openapi": "3.0.3",
    "info": {"title": "sapogin-corpus API", "version": "1.0.0",
             "description": "Search and explore 1,641 provenance-pinned claims from Sapogin's 'Canonical Physics' (LENR/EVO corpus). Also available as an MCP streamable-HTTP server at /mcp."},
    "servers": [{"url": "/"}],
    "paths": {
        "/api/search": {"get": {"summary": "Full-text claim search",
            "parameters": [
                {"name": "q", "in": "query", "schema": {"type": "string"}},
                {"name": "bucket", "in": "query", "schema": {"type": "string"}},
                {"name": "priority", "in": "query", "schema": {"type": "string", "enum": ["core", "normal"]}},
                {"name": "facet", "in": "query", "schema": {"type": "string"}},
                {"name": "doc", "in": "query", "schema": {"type": "string", "description": "doc_id e.g. AR04"}},
                {"name": "section", "in": "query", "schema": {"type": "string"}},
                {"name": "cluster", "in": "query", "schema": {"type": "string"}},
                {"name": "limit", "in": "query", "schema": {"type": "integer", "maximum": 100}}],
            "responses": {"200": {"description": "ranked claim results"}}}},
        "/api/claim/{id}": {"get": {"summary": "Full claim record",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "claim"}}}},
        "/api/clusters": {"get": {"summary": "List clusters", "responses": {"200": {"description": "clusters"}}}},
        "/api/cluster/{id}": {"get": {"summary": "Cluster detail",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "cluster"}}}},
        "/api/buckets": {"get": {"summary": "Bucket summary", "responses": {"200": {"description": "buckets"}}}},
        "/api/synthesis/{bucket}": {"get": {"summary": "Bucket synthesis markdown",
            "parameters": [{"name": "bucket", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "markdown"}}}},
        "/api/random": {"get": {"summary": "Random claim sample",
            "parameters": [{"name": "n", "in": "query", "schema": {"type": "integer"}},
                           {"name": "bucket", "in": "query", "schema": {"type": "string"}}],
            "responses": {"200": {"description": "claims"}}}},
        "/api/stats": {"get": {"summary": "Corpus overview", "responses": {"200": {"description": "stats"}}}},
    },
}


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8420
    load()
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"sapogin-corpus explorer + API on http://127.0.0.1:{port} "
          f"({N} claims, {len(clusters)} clusters, {len(synthesis)} syntheses)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
