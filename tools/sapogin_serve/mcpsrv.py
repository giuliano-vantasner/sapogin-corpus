"""MCP tool definitions and JSON-RPC dispatch over shared corpus queries."""
import json

from . import corpus

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
    if not corpus.has_query(a):
        return {"error": "empty query: pass q or at least one filter "
                         "(bucket, priority, facet, doc, section, cluster)"}
    return corpus.search_page(a, 15)

def _tool_claim(a):
    cid = str(a.get("id", "")).upper()
    claim = corpus.claim_by_id(cid)
    return claim if claim is not None else {"error": f"unknown claim id {cid}"}


def _tool_clusters(a):
    return corpus.clusters_list(a.get("bucket"))


def _tool_cluster(a):
    cluster = corpus.cluster_detail(a.get("id"))
    return cluster if cluster is not None else {
        "error": f"unknown cluster {a.get('id')}"}

def _tool_synthesis(a):
    bucket = a.get("bucket", "")
    markdown = corpus.synthesis_of(bucket)
    return {"bucket": bucket, "markdown": markdown} if markdown is not None else {
        "error": f"no synthesis for {bucket}",
        "available": sorted(corpus.synthesis)}



def _tool_stats(a):
    return corpus.stats_payload("")





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
