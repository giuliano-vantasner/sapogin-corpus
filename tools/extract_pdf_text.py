#!/usr/bin/env python3
"""Extract UTF-8 text from every papers/<section>/*.pdf into papers/text/.

Usage: python3 tools/extract_pdf_text.py [--force]
Requires poppler-utils (pdftotext). Non-PDF documents (djvu/doc) are skipped
with a notice; OCR fallback lives in the vision-ocr harness skill.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "papers" / "text"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ok = skipped = failed = 0
    for pdf in sorted((ROOT / "papers").glob("*/*.pdf")):
        rel = pdf.relative_to(ROOT / "papers")
        txt = OUT / (str(rel.with_suffix("")) + ".txt")
        txt.parent.mkdir(parents=True, exist_ok=True)
        if txt.exists() and not args.force:
            ok += 1
            continue
        r = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", "-layout", str(pdf), str(txt)],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and txt.exists() and txt.stat().st_size > 0:
            ok += 1
        else:
            failed += 1
            print(f"FAIL {rel}: {r.stderr.strip()[:200]}", file=sys.stderr)
            txt.unlink(missing_ok=True)
    for other in sorted(p for p in (ROOT / "papers").glob("*/*") if p.is_file() and p.suffix.lower() not in (".pdf", ".yaml", ".md")):
        skipped += 1
        print(f"SKIP {other.relative_to(ROOT)}: not a PDF (OCR/manual fallback needed)", file=sys.stderr)
    print(f"text extracted: {ok} ok, {skipped} skipped, {failed} failed -> {OUT}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
