#!/usr/bin/env python3
"""
Extract NIST source PDFs to Markdown using Marker.

Usage:
    python scripts/extract.py                  # Process every PDF in sources/
    python scripts/extract.py path/to/file.pdf # Process a single PDF
    python scripts/extract.py --force          # Re-extract even if output exists

Output layout:
    sources/extracted/<basename>/<basename>.md
    sources/extracted/<basename>/<basename>.sha256

The .sha256 file uses standard `sha256sum`-compatible format so that
`sha256sum -c <basename>.sha256` can verify the extracted Markdown later.
The same hex digest, prefixed with `sha256:`, is what each card's
`source_hash` field stores per cards/schema.json.

Marker is invoked via its CLI (`marker_single`). Install with:
    pipx install marker-pdf
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = REPO_ROOT / "sources"
EXTRACTED_DIR = SOURCES_DIR / "extracted"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_one(pdf_path: Path, force: bool = False) -> Path:
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF: {pdf_path}")

    basename = pdf_path.stem
    out_dir = EXTRACTED_DIR / basename
    out_md = out_dir / f"{basename}.md"
    out_hash = out_dir / f"{basename}.sha256"

    if out_md.exists() and not force:
        print(f"[skip] {pdf_path.name} (extraction exists; use --force to override)")
        return out_md

    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[extract] {pdf_path.name} -> {out_md.relative_to(REPO_ROOT)}")

    cmd = [
        "marker_single",
        str(pdf_path),
        "--output_dir", str(EXTRACTED_DIR),
        "--output_format", "markdown",
        # Our cards are text-only definitions. Skip image extraction so we
        # don't bloat the repo with rasterised figures we never cite. Re-run
        # without this flag if a card ever needs to reference a figure.
        "--disable_image_extraction",
    ]
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"marker_single exited {result.returncode}")

    if not out_md.exists():
        raise RuntimeError(f"Marker did not produce expected output: {out_md}")

    digest = sha256_of_file(out_md)
    out_hash.write_text(f"{digest}  {basename}.md\n")
    print(f"[hash]    sha256:{digest[:16]}...  {out_md.name}")

    return out_md


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract NIST source PDFs to Markdown via Marker."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="PDF file(s) to extract. If omitted, processes every PDF in sources/.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-extract even if the output already exists.",
    )
    args = parser.parse_args()

    if not shutil.which("marker_single"):
        print(
            "error: 'marker_single' not found in PATH. Install with:\n"
            "    pipx install marker-pdf",
            file=sys.stderr,
        )
        return 1

    if args.paths:
        targets = args.paths
    else:
        targets = sorted(SOURCES_DIR.glob("*.pdf"))
        if not targets:
            print(f"No PDFs found in {SOURCES_DIR}", file=sys.stderr)
            return 1

    for pdf in targets:
        try:
            extract_one(pdf, force=args.force)
        except Exception as exc:
            print(f"[fail] {pdf}: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
