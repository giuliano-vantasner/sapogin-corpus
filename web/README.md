# sapogin-corpus explorer + agent API

Human UI at `/` (cluster graph, browse index, full-text search, syntheses,
drag-resizable results panel). Agents get the same corpus two ways:

## 1. HTTP JSON API (any agent — curl, scripts, no browser)

Base: `http://127.0.0.1:8420` (loopback only; expose via Pangolin if needed)

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

Ranking: idf-weighted over statement (×2), tags (×3), quote (×1), exact-id
match (×25). Cyrillic fully supported (`q=протонные кластеры`).

```bash
curl -s 'http://127.0.0.1:8420/api/search?q=varicap%20capacitance&priority=core&limit=5'
curl -s http://127.0.0.1:8420/api/claim/SC-AR04-005
```

## 2. WebMCP (MCP-capable clients, e.g. Claude Desktop)

The page registers six tools via the WebMCP widget (bottom-right):
`search_claims`, `get_claim`, `list_clusters`, `get_cluster`,
`get_synthesis`, `corpus_stats`.

Connect: run `npx -y @jason.today/webmcp@latest --mcp` as an MCP server in
your client, generate a token, click the blue widget, paste the token. Tools
then appear in the client's tool list.

## Regenerate derived data

After claims/clusters/synthesis change:
`python3 tools/build_web.py` (web/data.js) — the API server reads sources
directly at startup; restart the `sapogin-web` service to reload.
