"""HTTP routing, static serving, JSON responses, and MCP transport."""
import gzip
import html
import json
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler

from . import corpus, mcpsrv, specs

ROOT = corpus.ROOT
WEB = corpus.WEB
claims = corpus.claims
clusters = corpus.clusters
cluster_payload = corpus.cluster_payload


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
            body = specs.LLMSTXT.replace("{BASE}", self._base()).encode()
            self._send(body, "text/markdown; charset=utf-8",
                       extra=(("Cache-Control", "no-store"),))
            return

        if path == "/robots.txt":
            self._send(specs.ROBOTS.encode(), "text/plain; charset=utf-8")
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
            spec = specs.openapi_spec()
            spec["servers"] = [{"url": self._base() + "/"}]
            return self._json(spec)

        if path.startswith("/claim/") or path.startswith("/cluster/"):
            kind, ident = path[1:].split("/", 1)
            return self._permalink(kind, ident)

        if not path.startswith("/api"):
            return self._static(path)

        if path == "/api/search":
            if not corpus.has_query(q):
                return self._json(
                    {"error": "empty query: pass q= or at least one filter "
                              "(bucket, priority, facet, doc, section, cluster)",
                     "hint": "see /openapi.json; full dump at /api/export.jsonl"}, 400)
            page = corpus.search_page(q, 20)
            return self._json({"query": q.get("q", ""), **page})

        if path.startswith("/api/claim/"):
            cid = path.rsplit("/", 1)[-1].upper()
            claim = corpus.claim_by_id(cid)
            if claim is not None:
                return self._json(claim)
            return self._json({"error": f"unknown claim id {cid}"}, 404)

        if path == "/api/clusters":
            return self._json(corpus.clusters_list())

        if path.startswith("/api/cluster/"):
            cid = path.rsplit("/", 1)[-1]
            cluster = corpus.cluster_detail(cid)
            if cluster is not None:
                return self._json(cluster)
            return self._json({"error": f"unknown cluster {cid}"}, 404)

        if path == "/api/buckets":
            return self._json(corpus.buckets_summary())

        if path.startswith("/api/synthesis/"):
            bucket = path.rsplit("/", 1)[-1]
            markdown = corpus.synthesis_of(bucket)
            if markdown is not None:
                return self._json({"bucket": bucket, "markdown": markdown})
            return self._json(
                {"error": f"no synthesis for {bucket}",
                 "available": sorted(corpus.synthesis)}, 404)

        if path == "/api/docs":
            return self._json(corpus.docs_payload())

        if path == "/api/export.json":
            return self._json(corpus.claims)

        if path == "/api/export.jsonl":
            body = "".join(json.dumps(claim, ensure_ascii=False) + "\n"
                           for claim in corpus.claims).encode()
            return self._send(body, "application/x-ndjson")

        if path == "/api/random":
            count = min(int(q.get("n", "5")), 50)
            return self._json(corpus.random_sample(count, q.get("bucket")))

        if path == "/api/stats":
            return self._json(corpus.stats_payload(self._base()))

        self._json({"error": "unknown endpoint", "try": "/api/stats"}, 404)

    # ---- MCP streamable HTTP (stateless, open) ----
    def mcp_endpoint(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            msg = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return self._json({"jsonrpc": "2.0", "id": None,
                               "error": {"code": -32700, "message": "Parse error"}}, 400)
        resp = mcpsrv.mcp_dispatch(msg)
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
