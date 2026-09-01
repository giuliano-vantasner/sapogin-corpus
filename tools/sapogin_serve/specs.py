"""Agent discovery text, robots policy, schemas, and OpenAPI generation."""
from . import corpus

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
    st = corpus.stats_payload("")
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
