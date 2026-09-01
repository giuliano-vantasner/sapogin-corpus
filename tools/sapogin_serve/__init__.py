"""sapogin-corpus serve package: corpus/query state, MCP server, specs, HTTP handler.

Decomposed from the former monolithic tools/serve_web.py. External behaviour
(routes, headers, response bytes) is unchanged; tools/serve_web.py stays the
entrypoint (`python tools/serve_web.py [port]`, binds 127.0.0.1:port).
"""
