# sapogin-corpus explorer + agent API

Human UI at `/` (cluster graph, browse index, full-text search, syntheses,
drag-resizable results panel). Agents get the same corpus three ways — all
open, no tokens, no auth:

## 1. MCP server (preferred): `POST /mcp`

Streamable-HTTP transport, JSON-RPC 2.0, stateless. Point any MCP client at:

```
http://127.0.0.1:8420/mcp
```

Tools: `search_claims`, `get_claim`, `list_clusters`, `get_cluster`,
`get_synthesis`, `corpus_stats`. Verified with the official `mcp` Python SDK
(`mcp.client.streamable_http`, protocol 2025-11-25). Claude Desktop / any
MCP client: add an HTTP-type MCP server with that URL — done, no widget, no
token.

## 2. JSON API

| Endpoint | Purpose |
|---|---|
| `/api/stats` | corpus overview + endpoint list |
| `/api/search?q=…` | full-text search: English statements, Russian quotes, tags, SC-* ids. Filters: `bucket`, `priority` (core/normal), `facet`, `doc`, `section`, `cluster`, `limit` (≤100) |
| `/api/claim/<SC-ID>` | full record: statement, quote_ru, quantities, materials, geometry, procedure_steps, measurements, schematic_refs, pdf path + page |
| `/api/clusters` | all 145 proposal clusters |
| `/api/cluster/<id>` | cluster meta + member claim ids |
| `/api/buckets` | 8 topic buckets with sizes |
| `/api/synthesis/<bucket>` | practical-first synthesis markdown |
| `/api/random?n=5[&bucket=]` | sample claims for exploration |

Machine-readable spec: `/openapi.json`. Ranking: idf-weighted over statement
(×2), tags (×3), quote (×1), exact-id match (×25). Cyrillic fully supported.

## 3. Discovery (how agents find this unprompted)

- `/llms.txt` — agent-readable site guide (llmstxt.org convention)
- `/robots.txt` — allows all, comments name the MCP + API endpoints
- `/.well-known/ai-plugin.json` — plugin-style manifest, auth: none
- `/openapi.json` — OpenAPI 3 spec of the whole API
- Every response carries `Link: </mcp>; rel="mcp-server"`
- `index.html` carries `<link rel="mcp-server">` + meta description

## Source PDFs

Under `/papers/<section>/<file>.pdf` (paths returned by the API), page
anchors like `papers/articles/x.pdf#page=5`.

## Regenerate derived data

After claims/clusters/synthesis change: `python3 tools/build_web.py`
(web/data.js for the UI). The API/MCP server reads sources at startup —
restart the `sapogin-web` service to reload.
