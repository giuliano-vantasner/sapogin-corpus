#!/usr/bin/env python3
"""Deterministic cluster titling/summarizing shared by serve_web.py (runtime)
and build_web.py (offline).

title:   top cluster keywords, capitalized — a stable handle, not a thesis.
summary: one sentence lifted from the core claim whose word set overlaps the
         cluster keywords most (ties broken by statement length closest to
         160 chars). Falls back to non-core members when a cluster has none.
"""

import re

WORD = re.compile(r"[a-z0-9\u0400-\u04ff]+")


def cluster_title(keywords):
    ws = [k for k in (keywords or [])[:3] if k]
    return " ".join(w.capitalize() for w in ws) if ws else "Cluster"


def _first_sentence(text):
    text = " ".join((text or "").split())
    for i, ch in enumerate(text):
        if ch in ".!?" and (i + 1 == len(text) or text[i + 1] == " "):
            if i + 1 >= 30:
                return text[:i + 1]
    return (text[:180] + "…") if len(text) > 180 else text


def cluster_summary(cluster, statement_of):
    """statement_of: claim id -> statement text."""
    core = [statement_of[c] for c in cluster.get("core_ids", []) if statement_of.get(c)]
    pool = core or [statement_of[c] for c in cluster.get("claim_ids", []) if statement_of.get(c)]
    if not pool:
        return ""
    kws = {w.lower() for k in cluster.get("keywords", []) for w in WORD.findall(k)}

    def key(s):
        toks = set(WORD.findall(s.lower()))
        return (-len(toks & kws), abs(len(s) - 160))

    return _first_sentence(max(pool, key=key))
