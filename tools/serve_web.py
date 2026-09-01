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
import gzip
import html
import json
import math
import random
import re
import sys
import time
import urllib.parse
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

from corpus_common import cluster_summary, cluster_title

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
    statement_of = {c["id"]: c["statement"] for c in claims}
    for c in clusters:
        c["title"] = cluster_title(c["keywords"])
        c["summary"] = cluster_summary(c, statement_of)
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
    server_version = "sapogin-corpus/1.0"   # don't advertise BaseHTTP/Python
    sys_version = ""

    def _send(self, body: bytes, ctype: str, code: int = 200, extra=()):
        head_only = getattr(self, "_head_only", False)
        if (not head_only and len(body) > 1024
                and "gzip" in (self.headers.get("Accept-Encoding") or "").lower()):
            body = gzip.compress(body)
            self.send_response(code)
            self.send_header("Content-Encoding", "gzip")
        else:
            self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Vary", "Accept-Encoding")
        self.send_header("Link", '</mcp>; rel="mcp-server"')
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(json.dumps(obj, ensure_ascii=False).encode(),
                   "application/json; charset=utf-8", code)

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
        ctype = {".html": "text/html", ".js": "text/javascript", ".css": "text/css",
                 ".json": "application/json", ".md": "text/markdown", ".yaml": "text/yaml",
                 ".svg": "image/svg+xml"}.get(f.suffix, "application/octet-stream")
        self._send(f.read_bytes(), f"{ctype}; charset=utf-8")

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
        self.send_header("Allow", "GET, POST")
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
            if self.command == "POST":
                return self.mcp_endpoint()
            if self.command in ("GET", "HEAD"):
                return self.mcp_sse()
            self.send_response(405)
            self.send_header("Allow", "GET, POST")
            self.end_headers()
            return

        if path == "/llms.txt" or path == "/.well-known/llms.txt":
            body = LLMSTXT.replace("{BASE}", self._base()).encode()
            self._send(body, "text/markdown; charset=utf-8",
                       extra=(("Cache-Control", "no-store"),))
            return

        if path == "/robots.txt":
            self._send(ROBOTS.encode(), "text/plain; charset=utf-8")
            return

        if path == "/sitemap.xml":
            base = self._base()
            urls = ["/", "/llms.txt", "/openapi.json", "/api/stats", "/api/docs",
                    "/api/export.json"]
            urls += [f"/cluster/{c['cluster']}" for c in clusters]
            urls += [f"/claim/{c['id']}" for c in claims]
            body = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    + "".join(f"<url><loc>{base}{u}</loc></url>\n" for u in urls)
                    + "</urlset>\n").encode()
            self._send(body, "application/xml; charset=utf-8",
                       extra=(("Cache-Control", "no-store"),))
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

        if path == "/.well-known/mcp.json":
            return self._json({
                "mcpServers": {"sapogin-corpus": {
                    "url": self._base() + "/mcp",
                    "transport": "streamable-http",
                    "auth": "none",
                    "description": "1,641 provenance-pinned LENR/EVO claims: "
                                   "search, clusters, syntheses (no auth, CORS open).",
                }}})

        if path == "/openapi.json":
            spec = openapi_spec()
            spec["servers"] = [{"url": self._base() + "/"}]
            return self._json(spec)

        if path.startswith("/claim/") or path.startswith("/cluster/"):
            kind, ident = path[1:].split("/", 1)
            return self._permalink(kind, ident)

        if not path.startswith("/api"):
            return self._static(path)

        if path == "/api/search":
            terms = tok(q.get("q", ""))
            filters = {k: q[k] for k in ("bucket", "priority", "facet", "doc",
                                         "section", "cluster") if q.get(k)}
            if not terms and not filters:
                return self._json(
                    {"error": "empty query: pass q= or at least one filter "
                              "(bucket, priority, facet, doc, section, cluster)",
                     "hint": "see /openapi.json; full dump at /api/export.jsonl"}, 400)
            hits = claims
            for k, v in filters.items():
                hits = [c for c in hits if c.get(k) == v]
            if terms:
                scored = [(score(c, terms), c) for c in hits]
                hits = [c for s, c in sorted(scored, key=lambda x: -x[0]) if s > 0]
            lim = min(int(q.get("limit", "20")), 100)
            off = max(int(q.get("offset", "0")), 0)
            return self._json({"query": q.get("q", ""), "total": len(hits), "offset": off,
                               "next_offset": off + lim if off + lim < len(hits) else None,
                               "results": hits[off:off + lim]})

        if path.startswith("/api/claim/"):
            cid = path.rsplit("/", 1)[-1].upper()
            for c in claims:
                if c["id"] == cid:
                    return self._json(c)
            return self._json({"error": f"unknown claim id {cid}"}, 404)

        if path == "/api/clusters":
            return self._json([cluster_payload(c, detail=False) for c in clusters])

        if path.startswith("/api/cluster/"):
            cid = path.rsplit("/", 1)[-1]
            for c in clusters:
                if c["cluster"] == cid:
                    return self._json(cluster_payload(c))
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

        if path == "/api/docs":
            return self._json(docs_payload())

        if path == "/api/export.json":
            return self._json(claims)

        if path == "/api/export.jsonl":
            body = "".join(json.dumps(c, ensure_ascii=False) + "\n"
                           for c in claims).encode()
            return self._send(body, "application/x-ndjson")

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

    def _wants_html(self):
        # JSON by default; HTML only when the client explicitly accepts it
        return "text/html" in (self.headers.get("Accept") or "").lower()

    def _permalink(self, kind, ident):
        # real permalink paths for hash permalinks: JSON for agents, HTML
        # redirect to the hash UI for browsers
        if kind == "claim":
            ident = ident.upper()
            found = next((c for c in claims if c["id"] == ident), None)
            api = f"/api/claim/{ident}"
        else:
            found = next((c for c in clusters if c["cluster"] == ident), None)
            api = f"/api/cluster/{ident}"
        if not self._wants_html():
            if found is None:
                return self._json({"error": f"unknown {kind} id {ident}",
                                   "hint": f"see {api} or /llms.txt"}, 404)
            return self._json(found if kind == "claim" else cluster_payload(found))
        frag = f"/#{kind}={urllib.parse.quote(ident)}"
        esc_i = html.escape(ident)
        if found is None:
            body = (f"<!doctype html><meta charset=\"utf-8\"><title>404</title>"
                    f"<p>Unknown {kind} <b>{esc_i}</b>. "
                    f"<a href=\"/\">Back to the explorer</a></p>").encode()
            return self._send(body, "text/html; charset=utf-8", 404)
        body = (f"<!doctype html><meta charset=\"utf-8\">"
                f"<title>{kind} {esc_i} — sapogin-corpus</title>"
                f"<meta http-equiv=\"refresh\" content=\"0;url={frag}\">"
                f"<p>Redirecting to the explorer permalink "
                f"<a href=\"{frag}\">{esc_i}</a>… Machine-readable JSON: "
                f"<a href=\"{html.escape(api)}\">{html.escape(api)}</a></p>"
                f"<script>location.replace({json.dumps(frag)})</script>").encode()
        self._send(body, "text/html; charset=utf-8")

    def mcp_sse(self):
        # streamable-HTTP clients may open a GET SSE channel first; this
        # server is stateless and pushes nothing, so hold the stream with
        # keepalive comments until the client goes away
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Link", '</mcp>; rel="mcp-server"')
        self.end_headers()
        if getattr(self, "_head_only", False):
            return
        try:
            self.wfile.write(b": sapogin-corpus mcp - stateless; POST JSON-RPC 2.0 to /mcp\n\n")
            self.wfile.flush()
            while True:
                time.sleep(15)
                self.wfile.write(b": keepalive\n\n")
                self.wfile.flush()
        except OSError:
            pass

    def log_message(self, *a):  # quiet
        pass



# ---- MCP server: tools over streamable HTTP, no auth ----
PROTOCOL_VERSION = "2025-06-18"

MCP_TOOLS = [
    {"name": "search_claims",
     "description": "Full-text search over the provenance-pinned Sapogin 'Canonical Physics' claims (English statements, Russian quotes, tags, SC-* ids). Filters: bucket, priority (core|normal), facet (theory|phenomenology|experiment|measurement|recipe|material|process|procedure|schematic|geometry), doc, section, cluster. Requires q or at least one filter; page with limit (<=100) + offset.",
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
         "limit": {"type": "integer", "default": 15, "maximum": 100},
         "offset": {"type": "integer", "default": 0, "minimum": 0}},
         "required": ["q"]},
     "examples": [{"q": "charge cluster catalysis", "priority": "core", "limit": 5},
                  {"q": "протонные кластеры", "limit": 5},
                  {"q": "displacement current", "bucket": "electrical-devices"}]},
    {"name": "get_claim",
     "description": "Full record of one claim by SC-* id: statement, verbatim quote_ru, quantities, materials, geometry, procedure_steps, measurements, schematic_refs, source pdf path+page.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "list_clusters",
     "description": "List all proposal clusters (id, title, one-line summary, bucket, size, core count, keywords, facets).",
     "inputSchema": {"type": "object", "properties": {"bucket": {"type": "string"}}}},
    {"name": "get_cluster",
     "description": "One cluster's meta: title, one-line summary, keywords, facets, and member claim ids.",
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
    filters = {k: a[k] for k in ("bucket", "priority", "facet", "doc", "section",
                                 "cluster") if a.get(k)}
    if not terms and not filters:
        return {"error": "empty query: pass q or at least one filter "
                         "(bucket, priority, facet, doc, section, cluster)"}
    hits = claims
    for k, v in filters.items():
        hits = [c for c in hits if c.get(k) == v]
    if terms:
        scored = [(score(c, terms), c) for c in hits]
        hits = [c for s, c in sorted(scored, key=lambda x: -x[0]) if s > 0]
    lim = min(int(a.get("limit", 15)), 100)
    off = max(int(a.get("offset", 0)), 0)
    return {"total": len(hits), "offset": off,
            "next_offset": off + lim if off + lim < len(hits) else None,
            "results": hits[off:off + lim]}


def _tool_claim(a):
    cid = str(a.get("id", "")).upper()
    for c in claims:
        if c["id"] == cid:
            return c
    return {"error": f"unknown claim id {cid}"}


def _tool_clusters(a):
    sel = [c for c in clusters if not a.get("bucket") or c["bucket"] == a["bucket"]]
    return [cluster_payload(c, detail=False) for c in sel]


def _tool_cluster(a):
    for c in clusters:
        if c["cluster"] == a.get("id"):
            return cluster_payload(c)
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
                    ["/api/search?q=", "/api/claim/<id>", "/claim/<id>",
                     "/api/clusters", "/api/cluster/<id>", "/api/buckets",
                     "/api/synthesis/<bucket>", "/api/docs", "/api/random?n=",
                     "/api/export.jsonl", "/api/stats"]]}


def _tool_stats(a):
    return stats_payload("")


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


def _mcp_text(name, p):
    # short human-readable summary; the full payload rides in structuredContent
    if isinstance(p, dict) and p.get("error"):
        return f"error: {p['error']}"
    if name == "search_claims":
        ids = ", ".join(r["id"] for r in p["results"][:8])
        more = "…" if len(p["results"]) > 8 else ""
        return (f"{p['total']} match(es); top {len(p['results'])}: {ids}{more}. "
                f"Full JSON in structuredContent.")
    if name == "get_claim":
        return f"{p['id']} [{p.get('doc')} p.{p.get('page')}] {p.get('statement', '')[:180]}"
    if name == "list_clusters":
        return (f"{len(p)} clusters. Full list (id, title, summary, bucket, "
                f"keywords) in structuredContent.")
    if name == "get_cluster":
        return f"{p['cluster']} ({p['bucket']}): {p['size']} claims — {p.get('summary', '')}"
    if name == "get_synthesis":
        return f"Synthesis for {p['bucket']}: {len(p['markdown'])} chars of markdown in structuredContent."
    if name == "corpus_stats":
        return (f"{p['claims']} claims, {p['sources']} sources, {p['clusters']} clusters, "
                f"{len(p['buckets'])} buckets. MCP at {p['mcp']}.")
    return json.dumps(p, ensure_ascii=False)[:400]


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
            "content": [{"type": "text", "text": _mcp_text(name, payload)}],
            "structuredContent": payload,
            **({"isError": True}
               if isinstance(payload, dict) and payload.get("error") else {})}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"Method not found: {method}"}}


LLMSTXT = """# sapogin-corpus

> 1,641 provenance-pinned source claims extracted from Vladimir Sapogin's
> "Canonical Physics" site and 54 papers (LENR / EVO / charge-cluster research),
> organized into 145 provisional clusters across 8 topic buckets, with
> practical-first syntheses. Every claim carries a verbatim Russian quote, an
> English rendering (statement), and a source path + page. Data, not doctrine.

All surfaces are open (no auth) and CORS-enabled.

## Surfaces

- MCP (preferred): streamable-HTTP JSON-RPC 2.0 at {BASE}/mcp — POST requests;
  GET opens an SSE keepalive stream (stateless server). Tools below.
- JSON API: {BASE}/api/… — see "JSON API". Machine-readable spec: {BASE}/openapi.json
- Human UI: {BASE}/ — graph + browse + search (JS app).
- Bulk: {BASE}/api/export.json (array of all claims) and {BASE}/api/export.jsonl
  (ndjson). Gzipped when the client sends Accept-Encoding: gzip. Optional dump:
  {BASE}/data.js (~2.5 MB `window.SAPOGIN = {{…}}`, same data + UI edges).
- Discovery: /llms.txt (this file, also /.well-known/llms.txt), /openapi.json,
  /sitemap.xml, /.well-known/mcp.json, /.well-known/ai-plugin.json, /robots.txt.

## MCP tools

- search_claims {q, bucket, priority, facet, doc, section, cluster, limit≤100, offset}
- get_claim {id} — full claim record by SC-* id
- list_clusters {bucket?} — all clusters with title + one-line summary
- get_cluster {id} — cluster meta + member claim ids
- get_synthesis {bucket} — practical-first synthesis markdown
- corpus_stats — counts, buckets, endpoint list

## JSON API

- GET /api/search?q=TERM[&bucket=&priority=&facet=&doc=&section=&cluster=&limit=&offset=]
- GET /api/claim/<SC-ID> — full claim record
- GET /api/clusters — all clusters (id, title, summary, bucket, size, keywords, facets)
- GET /api/cluster/<id> — cluster meta + core_ids + claim_ids
- GET /api/buckets — bucket summary
- GET /api/synthesis/<bucket> — raw synthesis markdown
- GET /api/docs — all 65 sources: doc_id, kind, title, path, claim counts
- GET /api/random?n=5[&bucket=]
- GET /api/export.json | /api/export.jsonl — full corpus dump
- GET /api/stats — corpus overview (start here)

Permalink paths (JSON for non-browser agents; browsers get a redirect to the
hash UI): {BASE}/claim/<SC-ID> and {BASE}/cluster/<id>. e.g.
  curl '{BASE}/claim/SC-TC03-019'
  curl '{BASE}/cluster/evo-charge-clusters-06'

## IDs, filters, buckets

- Claim id: SC-<DOC>-<NNN>, e.g. SC-AR04-005 (document AR04, claim 005).
- Cluster id: <bucket>-<NN>, e.g. evo-charge-clusters-06. Clusters are
  provisional keyword-bag proposals with a one-line summary — a stable map,
  not adjudicated verdicts.
- Buckets: transmutation-nuclear, catalysis, evo-charge-clusters,
  electrical-devices, discharge-plasma, emden-gravity-cosmic,
  foundations-canonical, general.
- priority: "core" (transmutation / catalysis / EVO / electrical path) | "normal".
- facet: theory, phenomenology, experiment, measurement, recipe, material,
  process, procedure, schematic, geometry.

## Claim record — what to trust

- statement: faithful English rendering; may retain Cyrillic symbols used in
  the source (e.g. Pвых).
- quote: verbatim Russian source quote. There is no separate quote_en field;
  statement is the English rendering.
- quantities / materials / geometry / steps / measurements / schematic_refs:
  frequently []. An empty array means NOT EXTRACTED — it does NOT mean "none
  exist in the source". Do not treat [] as absence of materials or numbers;
  read the quote (or the source scan) to check.
- tags: free-text keywords. doc + page locate the source.

## Examples

  curl '{BASE}/api/stats'
  curl '{BASE}/api/search?q=charge%20cluster%20catalysis&priority=core&limit=5'
  curl '{BASE}/api/claim/SC-AR04-005'
  curl '{BASE}/api/cluster/evo-charge-clusters-06'
  curl '{BASE}/api/docs'
  curl '{BASE}/api/export.jsonl' --compressed -o claims.jsonl
  curl '{BASE}/api/synthesis/catalysis'

MCP (raw JSON-RPC over POST {BASE}/mcp):
  {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}
  {"jsonrpc":"2.0","id":2,"method":"tools/list"}
  {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_claims",
   "arguments":{"q":"varicap capacitance","priority":"core","limit":5}}}
  {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_claim",
   "arguments":{"id":"SC-TC08-098"}}}

Typical agent flow: /api/stats → /api/search (facet=recipe or priority=core)
→ /api/claim/<id> for the verbatim quote + page → /api/synthesis/<bucket> for
the practical digest → fetch the source for full context.

## Source paths

- Papers: {BASE}/papers/<section>/<file>.pdf (fetchable; the browser fragment
  #page=N jumps to the claim's page).
- Site mirrors: {BASE}/site/<page>.md (markdown).
- /api/docs lists every source with its path and claim counts; each claim's
  `pdf` field gives its exact source path.
"""

ROBOTS = """User-agent: *
Allow: /

# Agents: MCP streamable-HTTP server at /mcp (JSON-RPC 2.0, no auth)
# JSON API: /api/search?q= ... see /llms.txt and /openapi.json
Sitemap: /sitemap.xml
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
        "pdf": {"type": "string",
                "description": "source path under /papers or /site (fetchable; browser fragment #page=N)"},
        "statement": {"type": "string",
                      "description": "faithful English rendering; may retain Cyrillic symbols used in the source (e.g. Pвых)"},
        "quote": {"type": "string",
                  "description": "verbatim Russian source quote; statement is the English rendering (no separate quote_en field)"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "quantities": {"type": "array", "items": {"type": "string"},
                       "description": "extracted numbers/quantities; [] = not extracted, NOT 'none in source'"},
        "materials": {"type": "array", "items": {"type": "string"},
                      "description": "extracted materials; [] = not extracted, NOT 'none in source'"},
        "geometry": {"type": "array", "items": {"type": "string"},
                     "description": "extracted geometry; [] = not extracted, NOT 'none in source'"},
        "steps": {"type": "array", "items": {"type": "string"},
                  "description": "extracted procedure steps; [] = not extracted, NOT 'none in source'"},
        "measurements": {"type": "array", "items": {"type": "string"},
                         "description": "extracted measurements; [] = not extracted, NOT 'none in source'"},
        "schematic_refs": {"type": "array", "items": {"type": "string"},
                           "description": "figure/schematic references; [] = not extracted, NOT 'none in source'"},
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
        "offset": {"type": "integer", "description": "start of the returned window", "example": 0},
        "next_offset": {"type": "integer", "nullable": True,
                        "description": "pass as offset= to page forward; null when exhausted"},
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

def openapi_spec():
    # generated from the same live objects as /api/stats — one source of truth
    st = stats_payload("")
    desc = (f"Search and explore {st['claims']} provenance-pinned claims from "
            f"Sapogin's 'Canonical Physics' (LENR/EVO corpus) across {st['sources']} "
            f"sources ({st['papers']} papers + {st['site_pages']} site pages), "
            f"{st['clusters']} provisional clusters in {len(st['buckets'])} buckets. "
            f"Live counts: /api/stats. Full dump: /api/export.json or /api/export.jsonl. "
            f"Also an MCP streamable-HTTP server at /mcp (POST JSON-RPC 2.0; GET opens "
            f"an SSE keepalive stream). Claim records: `quote` is the verbatim Russian "
            f"source line; `statement` is the English rendering; empty practical-layer "
            f"arrays mean NOT EXTRACTED, not 'none in source'.")
    return {
        "openapi": "3.0.3",
        "info": {"title": "sapogin-corpus API", "version": "1.1.0", "description": desc},
        "servers": [{"url": "/"}],
        "components": {"schemas": {
            "Claim": CLAIM_SCHEMA, "ClaimBrief": CLAIM_BRIEF,
            "SearchResponse": SEARCH_RESPONSE, "StatsResponse": STATS_RESPONSE,
            "Error": {"type": "object", "properties": {
                "error": {"type": "string"}, "hint": {"type": "string"}}},
            "Cluster": {"type": "object", "properties": {
                "cluster": {"type": "string", "example": "evo-charge-clusters-06"},
                "title": {"type": "string", "description": "short keyword-derived title"},
                "summary": {"type": "string",
                            "description": "one-sentence thesis, from the most keyword-central core claim"},
                "bucket": {"type": "string"}, "size": {"type": "integer"},
                "core": {"type": "integer"},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "facets": {"type": "array", "items": {"type": "string"}}}},
            "ClusterDetail": {"type": "object", "properties": {
                "cluster": {"type": "string"}, "title": {"type": "string"},
                "summary": {"type": "string"}, "bucket": {"type": "string"},
                "size": {"type": "integer"}, "core": {"type": "integer"},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "facets": {"type": "array", "items": {"type": "string"}},
                "core_ids": {"type": "array", "items": {"type": "string"}},
                "claim_ids": {"type": "array", "items": {"type": "string"}},
                "synthesis": {"type": "boolean", "description": "a bucket synthesis exists"}}},
            "Bucket": {"type": "object", "properties": {
                "bucket": {"type": "string"}, "clusters": {"type": "integer"},
                "claims": {"type": "integer"}}},
            "DocEntry": {"type": "object", "properties": {
                "doc_id": {"type": "string", "example": "AR04"},
                "kind": {"type": "string", "enum": ["paper", "site"]},
                "section": {"type": "string", "example": "articles"},
                "title": {"type": "string"},
                "path": {"type": "string",
                         "description": "fetchable path (/papers/… .pdf or /site/… .md)",
                         "example": "/papers/articles/example.pdf"},
                "bytes": {"type": "integer"},
                "claims": {"type": "integer", "description": "claims extracted from this document"},
                "core": {"type": "integer", "description": "core-priority claims"}}},
            "DocsResponse": {"type": "object", "properties": {
                "documents": {"type": "array",
                              "items": {"$ref": "#/components/schemas/DocEntry"}},
                "total": {"type": "integer"}}},
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
                     "description": "terms; required unless a filter is given",
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
                    {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 15, "maximum": 100}},
                    {"name": "offset", "in": "query", "schema": {"type": "integer", "default": 0, "minimum": 0}}],
                "responses": {
                    "200": {"description": "Ranked claims; `total` is the full match count, `results` capped at `limit` starting at `offset`; `next_offset` null when exhausted.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SearchResponse"}}}},
                    "400": {"description": "Empty query — pass q= or at least one filter.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}}}},
            "/api/claim/{id}": {"get": {"summary": "Full claim record",
                "parameters": [{"name": "id", "in": "path", "required": True,
                                "schema": {"type": "string"}, "example": "SC-AR04-005"}],
                "responses": {
                    "200": {"description": "The complete claim: English statement, verbatim Russian quote, practical-layer fields (empty = not extracted), source path+page.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Claim"}}}},
                    "404": {"description": "Unknown claim id.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}}}},
            "/claim/{id}": {"get": {"summary": "Claim permalink (JSON default; HTML redirect for browsers)",
                "description": "Content-negotiated: JSON (same payload as /api/claim/{id}) unless the client accepts text/html, in which case a small HTML page redirects to the /#claim={id} UI permalink.",
                "parameters": [{"name": "id", "in": "path", "required": True,
                                "schema": {"type": "string"}, "example": "SC-TC03-019"}],
                "responses": {
                    "200": {"description": "Claim record (JSON) or HTML redirect page (browsers).",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Claim"}}}},
                    "404": {"description": "Unknown claim id.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}}}},
            "/api/clusters": {"get": {"summary": "List clusters",
                "responses": {"200": {"description": "All provisional clusters with title + one-line summary.",
                                      "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Cluster"}}}}}}}},
            "/api/cluster/{id}": {"get": {"summary": "Cluster detail",
                "parameters": [{"name": "id", "in": "path", "required": True,
                                "schema": {"type": "string"}, "example": "evo-charge-clusters-06"}],
                "responses": {
                    "200": {"description": "Cluster meta + core_ids + claim_ids.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ClusterDetail"}}}},
                    "404": {"description": "Unknown cluster id.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}}}},
            "/cluster/{id}": {"get": {"summary": "Cluster permalink (JSON default; HTML redirect for browsers)",
                "parameters": [{"name": "id", "in": "path", "required": True,
                                "schema": {"type": "string"}, "example": "evo-charge-clusters-06"}],
                "responses": {
                    "200": {"description": "Cluster detail (JSON) or HTML redirect page (browsers).",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ClusterDetail"}}}},
                    "404": {"description": "Unknown cluster id.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}}}},
            "/api/buckets": {"get": {"summary": "Bucket summary",
                "responses": {"200": {"description": "Cluster/claim counts per bucket.",
                                      "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Bucket"}}}}}}}},
            "/api/synthesis/{bucket}": {"get": {"summary": "Bucket synthesis markdown (practical-first digest)",
                "parameters": [{"name": "bucket", "in": "path", "required": True,
                                "schema": {"type": "string"}, "example": "catalysis"}],
                "responses": {
                    "200": {"description": "Synthesis markdown",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Synthesis"}}}},
                    "404": {"description": "No synthesis for this bucket; error lists available buckets.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}}}},
            "/api/docs": {"get": {"summary": "All source documents (papers + site mirrors)",
                "responses": {"200": {"description": "Every source with doc_id, title, fetchable path and claim counts.",
                                      "content": {"application/json": {"schema": {"$ref": "#/components/schemas/DocsResponse"}}}}}}},
            "/api/export.json": {"get": {"summary": "Full corpus dump (JSON array of all claims)",
                "responses": {"200": {"description": "All claims; gzipped when Accept-Encoding: gzip.",
                                      "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Claim"}}}}}}}},
            "/api/export.jsonl": {"get": {"summary": "Full corpus dump (ndjson, one claim per line)",
                "responses": {"200": {"description": "application/x-ndjson; gzipped when Accept-Encoding: gzip.",
                                      "content": {"application/x-ndjson": {"schema": {"type": "string"}}}}}}},
            "/api/random": {"get": {"summary": "Random claim sample",
                "parameters": [{"name": "n", "in": "query", "schema": {"type": "integer", "default": 5, "maximum": 50}},
                               {"name": "bucket", "in": "query", "schema": {"type": "string"}}],
                "responses": {"200": {"description": "Random claims.",
                                      "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Claim"}}}}}}}},
            "/api/stats": {"get": {"summary": "Corpus overview (start here)",
                "responses": {"200": {"description": "Counts, bucket list, absolute endpoint URLs.",
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
