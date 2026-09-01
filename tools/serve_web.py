#!/usr/bin/env python3
"""Static file server + JSON API for the sapogin-corpus explorer.

Thin entrypoint. Implementation lives in sapogin_serve: corpus state/query
logic, MCP tools, discovery specs, and HTTP transport/routing remain separate.
The CLI continues to bind 127.0.0.1:PORT.
"""
import os
import sys
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sapogin_serve import corpus
from sapogin_serve.handler import Handler


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8420
    corpus.load()
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"sapogin-corpus explorer + API on http://127.0.0.1:{port} "
          f"({corpus.N} claims, {len(corpus.clusters)} clusters, "
          f"{len(corpus.synthesis)} syntheses)", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
