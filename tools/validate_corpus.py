#!/usr/bin/env python3
"""Validate the Sapogin corpus: schema, IDs, provenance, coverage, debt lint.

Usage: python3 tools/validate_corpus.py [--root PATH]
Exit code 0 iff all checks pass. Warnings do not fail the run.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = {
    "articles", "works", "monography", "dissertation", "brochure", "lectures",
    "patents", "teaching", "technologies", "perpetual_motion", "site",
}
TYPES = {"experimental", "physical", "physics", "mathematical"}
FACETS = {
    "theory", "phenomenology", "experiment", "measurement", "recipe",
    "material", "process", "procedure", "schematic", "geometry",
}
PRIORITIES = {"core", "normal"}
CORE_TOPICS = (
    "transmut", "изотоп", "catalys", "катализ", "evo", "кластер",
    "электрическ", "excess energy", "избыточн",
)
CLAIM_ID = re.compile(r"^SC-[A-Z]{2}\d{2}-\d{3}$")
DOC_ID = re.compile(r"^[A-Z]{2}\d{2}$")

errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    root = Path(args.root)

    # --- MD5SUMS index
    md5sums: dict[str, str] = {}
    sums_path = root / "papers" / "MD5SUMS"
    if sums_path.exists():
        for line in sums_path.read_text().splitlines():
            if line.strip():
                digest, rel = line.split(maxsplit=1)
                md5sums[rel.strip().lstrip("*")] = digest
    else:
        warn("papers/MD5SUMS missing (ok before downloads complete)")

    # --- MANIFEST doc_ids
    manifest_ids: set[str] = set()
    manifest_path = root / "papers" / "MANIFEST.yaml"
    if manifest_path.exists():
        manifest = yaml.safe_load(manifest_path.read_text()) or {}
        entries = manifest.get("documents", manifest if isinstance(manifest, list) else [])
        for e in entries or []:
            if e.get("doc_id"):
                manifest_ids.add(e["doc_id"])
    else:
        warn("papers/MANIFEST.yaml missing (ok before downloads complete)")

    seen_ids: set[str] = set()
    claim_files = sorted((root / "claims" / "source").glob("*.yaml"))
    covered: dict[str, str] = {}

    for cf in claim_files:
        data = yaml.safe_load(cf.read_text()) or {}
        if data.get("schema") != "sapogin-corpus/source-claims/1":
            err(f"{cf.name}: bad schema key {data.get('schema')!r}")
        doc = data.get("document", {})
        did = doc.get("doc_id", "")
        if not DOC_ID.match(did):
            err(f"{cf.name}: bad doc_id {did!r}")
        if did in covered:
            err(f"{cf.name}: duplicate doc_id {did} (also in {covered[did]})")
        covered[did] = cf.name
        if doc.get("section") not in SECTIONS:
            err(f"{cf.name}: bad section {doc.get('section')!r}")
        rel_file = doc.get("file", "")
        if rel_file and not (root / rel_file).exists():
            warn(f"{cf.name}: document file missing: {rel_file}")
        if rel_file and md5sums:
            digest = md5sums.get(rel_file)
            if digest and doc.get("md5") and digest != doc["md5"]:
                err(f"{cf.name}: md5 mismatch for {rel_file}: {doc['md5']} != {digest}")
        claims = data.get("claims") or []
        cov = data.get("coverage") or {}
        if cov.get("zero_claim_document"):
            if claims:
                err(f"{cf.name}: zero_claim_document=true but {len(claims)} claims present")
            continue
        if not claims:
            warn(f"{cf.name}: no claims and not marked zero_claim_document")
        for c in claims:
            cid = c.get("id", "")
            if not CLAIM_ID.match(cid):
                err(f"{cf.name}: bad claim id {cid!r}")
                continue
            if not cid.startswith(f"SC-{did}-"):
                err(f"{cf.name}: claim id {cid} does not match doc_id {did}")
            if cid in seen_ids:
                err(f"{cf.name}: duplicate claim id {cid}")
            seen_ids.add(cid)
            if c.get("type") not in TYPES:
                err(f"{cid}: bad type {c.get('type')!r}")
            if c.get("facet") not in FACETS:
                err(f"{cid}: bad facet {c.get('facet')!r}")
            if c.get("priority") not in PRIORITIES:
                err(f"{cid}: bad priority {c.get('priority')!r}")
            if c.get("page") is None and doc.get("section") != "site":
                err(f"{cid}: missing page")
            blob = norm_ws(
                " ".join([str(c.get("statement_en", "")), " ".join(map(str, c.get("tags") or []))])
            ).lower()
            if c.get("priority") == "core" and not any(t in blob for t in CORE_TOPICS):
                warn(f"{cid}: priority=core but no core topic apparent in statement/tags")
            if not norm_ws(c.get("quote_ru", "")):
                err(f"{cid}: empty quote_ru")
            if not norm_ws(c.get("statement_en", "")):
                err(f"{cid}: empty statement_en")
            for rel in c.get("relations") or []:
                target = rel.get("to")
                if target and target not in seen_ids:
                    pass  # forward refs allowed; closure check below
        # quote spot-check against extracted text when available
        txt_rel = rel_file.replace("papers/", "papers/text/").rsplit(".", 1)[0] + ".txt"
        txt_path = root / txt_rel
        if txt_path.exists():
            text = norm_ws(txt_path.read_text(errors="replace"))
            for c in claims:
                q = norm_ws(c.get("quote_ru", ""))
                if q and q not in text:
                    warn(f"{c.get('id')}: quote_ru not found verbatim in {txt_rel} (encoding/OCR drift?)")

    # --- relation closure
    for cf in claim_files:
        data = yaml.safe_load(cf.read_text()) or {}
        for c in data.get("claims") or []:
            for rel in c.get("relations") or []:
                if rel.get("to") and rel["to"] not in seen_ids:
                    warn(f"{c.get('id')}: relation target {rel['to']} not in corpus (yet)")

    # --- coverage
    cov_path = root / "claims" / "coverage.yaml"
    if cov_path.exists():
        cov = yaml.safe_load(cov_path.read_text()) or {}
        for did, entry in (cov.get("documents") or {}).items():
            if did not in covered and not (entry or {}).get("pending", False):
                warn(f"coverage: {did} listed but no claim file yet")
        for did, cf_name in covered.items():
            if did not in (cov.get("documents") or {}):
                err(f"coverage: {cf_name} ({did}) missing from claims/coverage.yaml")
    else:
        warn("claims/coverage.yaml missing")

    # --- debt lint
    debt_path = root / "governance" / "debt.yaml"
    if debt_path.exists():
        debt = yaml.safe_load(debt_path.read_text()) or {}
        for d in debt.get("entries") or []:
            for key in ("id", "status", "statement", "source_claims"):
                if not d.get(key):
                    err(f"debt {d.get('id', '?')}: missing {key}")

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"{len(claim_files)} claim files, {len(seen_ids)} claims, "
          f"{len(warnings)} warnings, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
