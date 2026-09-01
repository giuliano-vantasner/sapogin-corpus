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
import urllib.parse
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
    global claims, clusters, synthesis, bucket_of, DF, N, docs, N_doc_sources
    rows = [json.loads(l) for l in (ROOT / "claims" / "claims.jsonl").read_text().splitlines() if l.strip()]
    clusters = json.loads((ROOT / "clusters" / "clusters.json").read_text())
    claim_cluster = {cid: c["cluster"] for c in clusters for cid in c["claim_ids"]}
    bucket_of = {c["cluster"]: c["bucket"] for c in clusters}
    manifest = yaml.safe_load((ROOT / "papers" / "MANIFEST.yaml").read_text())
    docs = {d["doc_id"]: d for d in manifest["documents"]}
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
    sdir = ROOT / "synthesis"
    if sdir.is_dir():
        synthesis = {m.stem: m.read_text() for m in sorted(sdir.glob("*.md"))}
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


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        if getattr(self, "_head_only", False):
            body = b""
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
        for prefix, base in (("/papers/", ROOT / "papers"), ("/site/", ROOT / "site")):
            if path.startswith(prefix):
                f = (base / path[len(prefix):]).resolve()
                allowed = str(base.resolve())
                break
        else:
            f = (WEB / path.lstrip("/")).resolve()
            allowed = str(WEB.resolve())
        if not str(f).startswith(allowed) or not f.is_file():
            self._json({"error": "not found", "hint": "see /llms.txt"}, 404)
            return
        if getattr(self, "_head_only", False):
            body = b""
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

    def do_HEAD(self):
        self._head_only = True
        self.do_GET()

    def do_DELETE(self):
        # stateless server: nothing to terminate
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Mcp-Session-Id")
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_header("Content-Length", "0")
        self.end_headers()

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

    def _base(self):
        host = (self.headers.get("X-Forwarded-Host")
                or self.headers.get("Host") or "127.0.0.1:8420")
        proto = (self.headers.get("X-Forwarded-Proto")
                 or ("https" if "vantasner.io" in host else "http"))
        return f"{proto}://{host}"

    def route(self):
        path, _, qs = self.path.partition("?")
        path = self._utf8(path)
        q = {k: self._utf8(urllib.parse.unquote_plus(v))
             for k, v in (kv.split("=", 1) for kv in qs.split("&") if "=" in kv)}
        path = path.rstrip("/") or "/"

        if path == "/mcp":
            return self.mcp_endpoint()

        if path == "/llms.txt":
            body = LLMSTXT.replace("{BASE}", self._base()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
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

        if path == "/sitemap.xml":
            base = self._base()
            urls = ["/", "/llms.txt", "/openapi.json", "/api/stats"]
            urls += [f"/#cluster={c['cluster']}" for c in clusters]
            body = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    + "".join(f"<url><loc>{base}{u}</loc></url>\n" for u in urls)
                    + "</urlset>\n").encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/xml; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
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
            spec = json.loads(json.dumps(OPENAPI))
            spec["servers"] = [{"url": self._base() + "/"}]
            return self._json(spec)

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
            return self._json(stats_payload(self._base()))

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
        if msg.get("method") == "initialize":
            import uuid
            self._mcp_session = uuid.uuid4().hex
        if getattr(self, "_mcp_session", None):
            body = json.dumps(resp, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Mcp-Session-Id", self._mcp_session)
            self.send_header("Link", '</mcp>; rel="mcp-server"')
            self.end_headers()
            if not getattr(self, "_head_only", False):
                self.wfile.write(body)
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
         "q": {"type": "string", "examples": ["varicap capacitance",
              "протонные кластеры", "charge cluster"]},
         "bucket": {"type": "string", "examples": ["transmutation-nuclear",
              "electrical-devices"]},
         "priority": {"type": "string", "enum": ["core", "normal"]},
         "facet": {"type": "string", "examples": ["recipe", "measurement",
              "experiment", "geometry"]},
         "doc": {"type": "string", "examples": ["AR04", "TC08"]},
         "section": {"type": "string"},
         "cluster": {"type": "string"},
         "limit": {"type": "integer", "default": 15, "maximum": 100}},
         "required": ["q"]},
     "examples": [{"q": "charge cluster catalysis", "priority": "core", "limit": 5},
                  {"q": "протонные кластеры", "limit": 5},
                  {"q": "displacement current", "bucket": "electrical-devices"}]},
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


def stats_payload(base: str) -> dict:
    n_site = sum(1 for d in docs.values() if d.get("section") == "site")
    return {"claims": N, "sources": N_doc_sources, "papers": N_doc_sources - n_site,
            "site_pages": n_site, "clusters": len(clusters),
            "buckets": sorted(set(bucket_of.values())),
            "core": sum(1 for c in claims if c["priority"] == "core"),
            "syntheses": sorted(synthesis),
            "mcp": base + "/mcp",
            "api": [base + e for e in
                    ["/api/search?q=", "/api/claim/<id>", "/api/clusters",
                     "/api/cluster/<id>", "/api/buckets", "/api/synthesis/<bucket>",
                     "/api/random?n=", "/api/stats"]]}


def _tool_stats(a):
    return stats_payload("")


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
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=1)}],
            "structuredContent": payload}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"Method not found: {method}"}}


LLMSTXT = """# sapogin-corpus

> 1,641 provenance-pinned source claims extracted from Vladimir Sapogin's
> "Canonical Physics" site and 54 papers (LENR / EVO / charge-cluster research),
> organized into 145 proposal clusters across 8 topic buckets, with
> practical-first syntheses. Data, not doctrine: every claim carries a verbatim
> Russian quote, English translation, and source-PDF page reference.

Agents can explore three ways, all open (no auth):

1. MCP (preferred): streamable-HTTP server at {BASE}/mcp — tools:
   search_claims, get_claim, list_clusters, get_cluster, get_synthesis,
   corpus_stats. Point any MCP client at {BASE}/mcp (POST, JSON-RPC 2.0).
2. JSON API: {BASE}/api/search?q= (filters: bucket, priority, facet, doc,
   section, cluster, limit), {BASE}/api/claim/<SC-ID>, {BASE}/api/clusters,
   {BASE}/api/cluster/<id>, {BASE}/api/buckets,
   {BASE}/api/synthesis/<bucket>, {BASE}/api/random?n=, {BASE}/api/stats.
   Machine-readable spec: {BASE}/openapi.json
   UI permalinks: {BASE}/#cluster=<cluster-id> or {BASE}/#claim=<SC-ID>
3. Human UI: / (graph + browse + search; agents may also read web/data.js).

Key buckets: transmutation-nuclear, catalysis, evo-charge-clusters,
electrical-devices, discharge-plasma, emden-gravity-cosmic,
foundations-canonical, general. Priority "core" = transmutation / catalysis /
EVO / electrical path.

Practical layer first: recipes, materials, geometry, procedures, measurements.
Sources: /papers/<section>/<file>.pdf and /site/<page>.md (paths returned by
the API; fetchable directly).

## Worked examples

JSON API:
  curl '{BASE}/api/search?q=charge%20cluster%20catalysis&priority=core&limit=5'
  curl '{BASE}/api/claim/SC-AR04-005'
  curl '{BASE}/api/synthesis/catalysis'
  curl '{BASE}/api/stats'

MCP (raw JSON-RPC over POST {BASE}/mcp):
  {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}
  {"jsonrpc":"2.0","id":2,"method":"tools/list"}
  {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_claims",
   "arguments":{"q":"varicap capacitance","priority":"core","limit":5}}}
  {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_claim",
   "arguments":{"id":"SC-TC08-098"}}}

Typical agent flow: /api/stats -> /api/search (facet=recipe or priority=core)
-> /api/claim/<id> for verbatim quote + page -> /api/synthesis/<bucket> for
the practical digest -> fetch the source PDF/text for full context.
"""

ROBOTS = """User-agent: *
Allow: /

# Agents: MCP streamable-HTTP server at /mcp (JSON-RPC 2.0, no auth)
# JSON API: /api/search?q= ... see /llms.txt and /openapi.json
"""

CLAIM_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "SC-* claim id", "example": "SC-AR04-005"},
        "cluster": {"type": "string", "example": "transmutation-nuclear-02"},
        "bucket": {"type": "string", "example": "transmutation-nuclear"},
        "doc": {"type": "string", "description": "document id", "example": "AR04"},
        "title": {"type": "string", "description": "English document title"},
        "section": {"type": "string", "example": "articles"},
        "type": {"type": "string", "description": "claim type",
                 "enum": ["experimental", "physical", "physics", "mathematical", "phenomenological"]},
        "facet": {"type": "string",
                  "description": "practical-layer facet",
                  "enum": ["theory", "phenomenology", "experiment", "measurement",
                           "recipe", "material", "process", "procedure", "schematic", "geometry"]},
        "priority": {"type": "string", "enum": ["core", "normal"]},
        "page": {"type": "integer"},
        "pdf": {"type": "string", "description": "source path under /papers or /site (fetchable)"},
        "statement": {"type": "string", "description": "faithful English rendering"},
        "quote": {"type": "string", "description": "verbatim source-language quote"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "quantities": {"type": "array", "items": {"type": "string"}},
        "materials": {"type": "array", "items": {"type": "string"}},
        "geometry": {"type": "array", "items": {"type": "string"}},
        "steps": {"type": "array", "items": {"type": "string"},
                  "description": "extracted procedure steps"},
        "measurements": {"type": "array", "items": {"type": "string"}},
        "schematic_refs": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["id", "statement"],
}

CLAIM_BRIEF = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "example": "SC-AR04-005"},
        "cluster": {"type": "string"}, "bucket": {"type": "string"},
        "doc": {"type": "string"}, "page": {"type": "integer"},
        "priority": {"type": "string"}, "statement": {"type": "string"},
        "pdf": {"type": "string"},
    },
}

SEARCH_RESPONSE = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "total": {"type": "integer", "description": "all matches (results are capped by limit)",
                  "example": 67},
        "results": {"type": "array", "items": CLAIM_BRIEF},
    },
}

STATS_RESPONSE = {
    "type": "object",
    "properties": {
        "claims": {"type": "integer", "example": 1641},
        "sources": {"type": "integer", "description": "papers + site pages", "example": 65},
        "papers": {"type": "integer", "example": 54},
        "site_pages": {"type": "integer", "example": 11},
        "clusters": {"type": "integer", "example": 145},
        "buckets": {"type": "array", "items": {"type": "string"}},
        "core": {"type": "integer", "description": "core-priority claim count", "example": 980},
        "syntheses": {"type": "array", "items": {"type": "string"}},
        "mcp": {"type": "string", "description": "absolute MCP endpoint"},
        "api": {"type": "array", "items": {"type": "string"},
                "description": "absolute endpoint templates"},
    },
}

OPENAPI = {
    "openapi": "3.0.3",
    "info": {"title": "sapogin-corpus API", "version": "1.0.0",
             "description": "Search and explore 1,641 provenance-pinned claims from Sapogin's 'Canonical Physics' (LENR/EVO corpus). Also available as an MCP streamable-HTTP server at /mcp."},
    "servers": [{"url": "/"}],
    "components": {"schemas": {
        "Claim": CLAIM_SCHEMA, "ClaimBrief": CLAIM_BRIEF,
        "SearchResponse": SEARCH_RESPONSE, "StatsResponse": STATS_RESPONSE,
        "Cluster": {"type": "object", "properties": {
            "cluster": {"type": "string", "example": "evo-charge-clusters-06"},
            "bucket": {"type": "string"}, "size": {"type": "integer"},
            "core": {"type": "integer"},
            "keywords": {"type": "array", "items": {"type": "string"}}}},
        "Synthesis": {"type": "object", "properties": {
            "bucket": {"type": "string", "example": "catalysis"},
            "markdown": {"type": "string", "description": "practical-first synthesis, GFM"}},
        },
    }},
    "paths": {
        "/api/search": {"get": {"summary": "Full-text claim search (idf-ranked)",
            "parameters": [
                {"name": "q", "in": "query", "required": True,
                 "schema": {"type": "string"},
                 "examples": {"en": {"value": "charge cluster catalysis"},
                              "ru": {"value": "протонные кластеры"}}},
                {"name": "bucket", "in": "query", "schema": {"type": "string"},
                 "examples": {"v": {"value": "electrical-devices"}}},
                {"name": "priority", "in": "query", "schema": {"type": "string", "enum": ["core", "normal"]}},
                {"name": "facet", "in": "query", "schema": {"type": "string",
                 "enum": ["theory", "phenomenology", "experiment", "measurement",
                          "recipe", "material", "process", "procedure", "schematic", "geometry"]}},
                {"name": "doc", "in": "query", "schema": {"type": "string", "description": "doc_id e.g. AR04"}},
                {"name": "section", "in": "query", "schema": {"type": "string"}},
                {"name": "cluster", "in": "query", "schema": {"type": "string"}},
                {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 15, "maximum": 100}}],
            "responses": {"200": {"description": "Ranked claims; `total` is the full match count, `results` capped at `limit`.",
                                  "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SearchResponse"}}}}}}},
        "/api/claim/{id}": {"get": {"summary": "Full claim record",
            "parameters": [{"name": "id", "in": "path", "required": True,
                            "schema": {"type": "string"}, "example": "SC-AR04-005"}],
            "responses": {"200": {"description": "The complete claim: statement, verbatim quote, practical-layer fields, source path+page.",
                                  "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Claim"}}}}}}},
        "/api/clusters": {"get": {"summary": "List clusters",
            "responses": {"200": {"description": "All 145 proposal clusters",
                                  "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Cluster"}}}}}}}},
        "/api/cluster/{id}": {"get": {"summary": "Cluster detail",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "cluster"}}}},
        "/api/buckets": {"get": {"summary": "Bucket summary", "responses": {"200": {"description": "buckets"}}}},
        "/api/synthesis/{bucket}": {"get": {"summary": "Bucket synthesis markdown (practical-first digest)",
            "parameters": [{"name": "bucket", "in": "path", "required": True,
                            "schema": {"type": "string"}, "example": "catalysis"}],
            "responses": {"200": {"description": "Synthesis markdown",
                                  "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Synthesis"}}}}}}},
        "/api/random": {"get": {"summary": "Random claim sample",
            "parameters": [{"name": "n", "in": "query", "schema": {"type": "integer"}},
                           {"name": "bucket", "in": "query", "schema": {"type": "string"}}],
            "responses": {"200": {"description": "claims"}}}},
        "/api/stats": {"get": {"summary": "Corpus overview (start here)",
            "responses": {"200": {"description": "Counts, bucket list, absolute endpoint URLs",
                                  "content": {"application/json": {"schema": {"$ref": "#/components/schemas/StatsResponse"}}}}}}},
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
