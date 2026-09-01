#!/usr/bin/env python3
"""Characterization (golden-master) harness for the serve_web refactor.

Captures a behaviour fingerprint of the running server: for a fixed set of
routes / methods / MCP calls it records `METHOD path | status | stable-headers
| sha256(body)[:16]`. Diffing the fingerprint from two builds proves they are
byte-for-byte identical on the wire — the safety proof behind the
`serve_web.py` -> `sapogin_serve` decomposition.

Volatile fields are normalized so the fingerprint is deterministic:
  * `Mcp-Session-Id` -> `<SID>`   (fresh uuid4 per initialize)
  * `/api/random` body           -> `<RANDOM>` (and its Content-Length dropped)

Usage:
    # baseline (e.g. on origin/main)
    python tools/serve_web.py 8420 &
    SAPOGIN_GOLDEN_HOST=sapogin.giuliano.vantasner.io \
      SAPOGIN_GOLDEN_PROTO=https \
      python tools/golden_master.py http://127.0.0.1:8420 > /tmp/golden_before.txt

    # candidate (refactor branch or a new deployed baseline)
    python tools/serve_web.py 8420 &
    SAPOGIN_GOLDEN_HOST=sapogin.giuliano.vantasner.io \
      SAPOGIN_GOLDEN_PROTO=https \
      python tools/golden_master.py http://127.0.0.1:8420 > /tmp/golden_after.txt

    diff /tmp/golden_before.txt /tmp/golden_after.txt   # empty == identical

The optional environment variables above replay every request with Pangolin's
`X-Forwarded-Host` and `X-Forwarded-Proto`. Set them to the same values for
parallel baseline/candidate servers so absolute-URL bodies are comparable.

Two fixtures below (CLUSTER, PDF) reference real corpus artifacts; update them
if the corpus is re-clustered or the sample PDF is renamed.
"""
import gzip
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

BASE = sys.argv[1].rstrip("/")
FORWARDED_HOST = os.environ.get("SAPOGIN_GOLDEN_HOST")
FORWARDED_PROTO = os.environ.get("SAPOGIN_GOLDEN_PROTO")
HDRS = ["Content-Type","Content-Length","Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods","Access-Control-Allow-Headers",
        "Access-Control-Max-Age","Allow","Cache-Control","Content-Encoding",
        "Vary","Link","Mcp-Session-Id"]
def req(method, path, body=None, ctype=None, headers=None):
    url = BASE + path
    data = body.encode() if isinstance(body,str) else body
    r = urllib.request.Request(url, data=data, method=method)
    if ctype: r.add_header("Content-Type", ctype)
    if FORWARDED_HOST: r.add_header("X-Forwarded-Host", FORWARDED_HOST)
    if FORWARDED_PROTO: r.add_header("X-Forwarded-Proto", FORWARDED_PROTO)
    for name, value in (headers or {}).items(): r.add_header(name, value)
    try:
        resp = urllib.request.urlopen(r, timeout=30)
        code = resp.getcode(); hd = resp.headers; raw = resp.read()
    except urllib.error.HTTPError as e:
        code = e.code; hd = e.headers; raw = e.read()
    parts=[]
    for h in HDRS:
        v = hd.get(h)
        if v is None: continue
        if h == "Mcp-Session-Id": v = "<SID>"
        parts.append(f"{h}={v}")
    if code == 204:
        # Pangolin legitimately strips Content-Length: 0 on no-content replies.
        parts = [p for p in parts if not p.startswith("Content-Length")]
    if path.startswith("/api/random"):
        bh = "<RANDOM>"; parts=[p for p in parts if not p.startswith("Content-Length")]
    else:
        stable_body = gzip.decompress(raw) if hd.get("Content-Encoding") == "gzip" else raw
        bh = hashlib.sha256(stable_body).hexdigest()[:16]
    return f"{method} {path} | {code} | {';'.join(parts)} | {bh}"

CLUSTER="evo-charge-clusters-01"
PDF="/papers/articles/bivolnovaya-priroda-printsipa-naimenshego-deystviya-relyativistskoy-chastitsy-za.pdf"
R=[]
for m,p in [("GET","/"),("GET","/app.js"),("GET","/data.js"),
    ("GET","/vendor/vis-network.min.js"),("GET","/site/home.md"),
    ("GET","/llms.txt"),("GET","/.well-known/llms.txt"),("GET","/openapi.json"),
    ("GET","/robots.txt"),("GET","/sitemap.xml"),
    ("GET","/.well-known/ai-plugin.json"),("GET","/.well-known/mcp"),
    ("GET","/.well-known/mcp.json"),
    ("GET","/api/stats"),("GET","/api/buckets"),("GET","/api/clusters"),
    ("GET","/api/docs"),("GET","/api/export.json"),("GET","/api/export.jsonl"),
    ("GET","/api/search?q=charge%20cluster%20catalysis&priority=core&limit=3"),
    ("GET","/api/search?q=%D0%BF%D1%80%D0%BE%D1%82%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%BB%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%8B&limit=4"),
    ("GET","/api/search"),
    ("GET","/api/claim/SC-AR04-005"),("GET","/api/claim/sc-ar04-005"),("GET","/api/claim/NOPE-999"),
    ("GET","/claim/SC-AR04-005"),("GET","/claim/NOPE-999"),
    ("GET",f"/api/cluster/{CLUSTER}"),("GET","/api/cluster/NOPE"),
    ("GET",f"/cluster/{CLUSTER}"),("GET","/cluster/NOPE"),
    ("GET","/api/synthesis/catalysis"),("GET","/api/synthesis/nope"),
    ("GET","/api/random?n=3"),("GET","/api/bogus"),
    ("GET","/../etc/passwd"),("GET","/papers/../../tools/serve_web.py"),
    ("HEAD","/"),("HEAD",PDF),("HEAD","/api/stats"),("HEAD","/mcp"),
    ("OPTIONS","/mcp"),("DELETE","/mcp"),
    ("POST","/api/search")]:
    R.append(req(m,p))
# MCP POSTs
for label,obj in [
    ("init",{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}),
    ("tools_list",{"jsonrpc":"2.0","id":2,"method":"tools/list"}),
    ("call_search",{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_claims","arguments":{"q":"varicap capacitance","priority":"core","limit":2}}}),
    ("call_search_empty",{"jsonrpc":"2.0","id":31,"method":"tools/call","params":{"name":"search_claims","arguments":{}}}),
    ("call_claim",{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_claim","arguments":{"id":"sc-tc08-098"}}}),
    ("call_badtool",{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"nope","arguments":{}}}),
    ("ping",{"jsonrpc":"2.0","id":6,"method":"ping"}),
    ("notif",{"jsonrpc":"2.0","method":"notifications/initialized"}),
    ("badmethod",{"jsonrpc":"2.0","id":7,"method":"zzz"})]:
    R.append("MCP:"+label+" | "+req("POST","/mcp",json.dumps(obj),"application/json"))
R.append("MCP:badjson | "+req("POST","/mcp","{not json","application/json"))
R.append("HTML:claim | "+req("GET","/claim/SC-AR04-005",headers={"Accept":"text/html"}))
R.append("HTML:cluster | "+req("GET",f"/cluster/{CLUSTER}",headers={"Accept":"text/html"}))
R.append("GZIP:export | "+req("GET","/api/export.jsonl",headers={"Accept-Encoding":"gzip"}))
print("\n".join(R))
