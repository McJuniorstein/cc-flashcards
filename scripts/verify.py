#!/usr/bin/env python3
"""
Verify flashcard JSON files against their cited NIST source extractions.

Usage:
    python scripts/verify.py                 # verify every cards/*.json
    python scripts/verify.py cards/x.json    # verify one card

For every card the verifier checks:

    1. JSON parses and the required schema fields are present with valid types
       and values (no jsonschema dependency - manual checks against
       cards/schema.json).
    2. source_hash matches a known extracted source under sources/extracted/.
       The hash itself is the link from card to source - source_doc is for
       humans.
    3. For answer_type=verbatim:
         a. source_excerpt appears as a contiguous substring of the extracted
            source markdown.
         b. back is byte-identical to source_excerpt.
    4. For answer_type=paraphrased:
         Skipped here. Paraphrased cards rely on human PR review per AGENTS.md.
         The verifier reports them so they aren't silently auto-approved.

Exit code is 0 if every card passes (or is correctly flagged for human review),
non-zero if any card fails a check that's the verifier's responsibility.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = REPO_ROOT / "cards"
EXTRACTED_DIR = REPO_ROOT / "sources" / "extracted"

REQUIRED_FIELDS = {
    "id": str,
    "front": str,
    "back": str,
    "source_doc": str,
    "source_excerpt": str,
    "answer_type": str,
    "primary_domain": int,
    "status": str,
    "created_at": str,
}

VALID_ANSWER_TYPES = {"verbatim", "paraphrased"}
VALID_STATUSES = {"draft", "verified", "active", "deprecated"}
ID_RE = re.compile(r"^cc-[a-z0-9]{6,}$")
HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class CardError(Exception):
    """A check the verifier owns failed for this card."""


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_known_sources() -> dict[str, Path]:
    """Map each known source hex digest to its .md path by scanning .sha256 files."""
    known: dict[str, Path] = {}
    if not EXTRACTED_DIR.exists():
        return known
    for sha_file in EXTRACTED_DIR.rglob("*.sha256"):
        first = sha_file.read_text().split(None, 1)[0]
        md = sha_file.with_suffix(".md")
        if md.exists():
            known[first] = md
    return known


def validate_schema(card: dict, path: Path) -> None:
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in card:
            raise CardError(f"missing required field '{field}'")
        if not isinstance(card[field], expected_type):
            raise CardError(
                f"field '{field}' has type {type(card[field]).__name__}, "
                f"expected {expected_type.__name__}"
            )

    if not ID_RE.match(card["id"]):
        raise CardError(f"id '{card['id']}' does not match {ID_RE.pattern}")
    if card["id"] != path.stem:
        raise CardError(f"id '{card['id']}' does not match filename stem '{path.stem}'")
    if card["answer_type"] not in VALID_ANSWER_TYPES:
        raise CardError(f"answer_type must be one of {sorted(VALID_ANSWER_TYPES)}")
    if card["status"] not in VALID_STATUSES:
        raise CardError(f"status must be one of {sorted(VALID_STATUSES)}")
    if not (1 <= card["primary_domain"] <= 5):
        raise CardError("primary_domain must be in 1..5")

    source_hash = card.get("source_hash")
    if source_hash is not None and not HASH_RE.match(source_hash):
        raise CardError(f"source_hash must match {HASH_RE.pattern}")


def verify_card(path: Path, known_sources: dict[str, Path]) -> tuple[str, str]:
    """Return (status, message) for one card. status in {ok, paraphrased, fail}."""
    try:
        card = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return "fail", f"invalid JSON: {exc}"

    try:
        validate_schema(card, path)
    except CardError as exc:
        return "fail", f"schema: {exc}"

    source_hash = card.get("source_hash")
    if not source_hash:
        return "fail", "missing source_hash (cannot resolve source)"
    digest = source_hash.split(":", 1)[1]
    md_path = known_sources.get(digest)
    if md_path is None:
        return "fail", f"no extracted source matches hash {digest[:16]}..."

    # Re-check the file on disk matches the stored hash (catches silent mutation).
    actual = sha256_of_file(md_path)
    if actual != digest:
        return "fail", (
            f"hash mismatch for {md_path.name}: card says {digest[:16]}..., "
            f"file is {actual[:16]}..."
        )

    excerpt = card["source_excerpt"]
    md_text = md_path.read_text()

    if card["answer_type"] == "paraphrased":
        return "paraphrased", "paraphrased card - human PR review required"

    # answer_type == verbatim
    if excerpt not in md_text:
        return "fail", "source_excerpt not found as substring in extracted source"
    if card["back"] != excerpt:
        return "fail", "back != source_excerpt (verbatim cards must match byte-for-byte)"

    return "ok", "verbatim match"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify CC Flashcard JSON files against their NIST source extractions."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Card JSON file(s). If omitted, verifies every cards/cc-*.json (schema.json is excluded by glob).",
    )
    args = parser.parse_args()

    if args.paths:
        targets = args.paths
    else:
        targets = sorted(CARDS_DIR.glob("cc-*.json"))
        if not targets:
            print(f"No cards found in {CARDS_DIR}", file=sys.stderr)
            return 1

    known_sources = load_known_sources()
    if not known_sources:
        print(
            "warning: no extracted sources found under sources/extracted/. "
            "Run scripts/extract.py first.",
            file=sys.stderr,
        )

    counts = {"ok": 0, "paraphrased": 0, "fail": 0}
    failures: list[tuple[Path, str]] = []

    for card_path in targets:
        status, message = verify_card(card_path, known_sources)
        counts[status] += 1
        marker = {"ok": "[ ok ]", "paraphrased": "[para]", "fail": "[FAIL]"}[status]
        print(f"{marker} {card_path.name}: {message}")
        if status == "fail":
            failures.append((card_path, message))

    total = sum(counts.values())
    print(
        f"\n{total} card(s): {counts['ok']} verified, "
        f"{counts['paraphrased']} awaiting human review, "
        f"{counts['fail']} failed"
    )

    return 0 if counts["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
