#!/usr/bin/env python3
"""
Build the static CC Flashcards app.

Reads card JSON files from cards/, filters out deprecated cards, and writes
a single cards.json to app/dist/. Copies static assets (HTML, CSS, JS, service
worker) from app/src/ to app/dist/.

The output of this script is exactly what gets served by Netlify. See
netlify.toml `publish = "app/dist"`.

Usage:
    python3 scripts/build_app.py            # standard build
    python3 scripts/build_app.py --include-drafts   # include draft cards too
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = REPO_ROOT / "cards"
SRC_DIR = REPO_ROOT / "app" / "src"
DIST_DIR = REPO_ROOT / "app" / "dist"

# Card statuses that appear in the deck. Deprecated is excluded.
STATUSES_SHOWN_DEFAULT = {"verified", "active", "draft"}
STATUSES_SHOWN_STRICT = {"verified", "active"}

# Static assets to copy from src/ to dist/. Anything not in this list is ignored
# so a stray file in src/ can't accidentally ship.
STATIC_ASSETS = ("index.html", "app.js", "style.css", "service-worker.js")


def load_cards(include_drafts: bool) -> list[dict]:
    """Return the deck as a list of card dicts, sorted by domain then front."""
    allowed = STATUSES_SHOWN_DEFAULT if include_drafts else STATUSES_SHOWN_STRICT
    cards: list[dict] = []
    for path in sorted(CARDS_DIR.glob("cc-*.json")):
        card = json.loads(path.read_text())
        if card.get("status") not in allowed:
            continue
        # The app only needs a subset of the card record. Strip extraction
        # provenance (source_excerpt, source_hash) from what we ship to keep
        # the payload small. source_doc, source_section, and source_chain stay
        # because they're rendered on the card back.
        cards.append({
            "id": card["id"],
            "front": card["front"],
            "back": card["back"],
            "source_doc": card["source_doc"],
            "source_section": card.get("source_section"),
            "source_chain": card.get("source_chain", []),
            "answer_type": card["answer_type"],
            "primary_domain": card["primary_domain"],
        })
    cards.sort(key=lambda c: (c["primary_domain"], c["front"].lower()))
    return cards


def write_dist(cards: list[dict]) -> None:
    """Write cards.json and copy static assets into app/dist/."""
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    cards_path = DIST_DIR / "cards.json"
    cards_path.write_text(json.dumps(cards, ensure_ascii=False, separators=(",", ":")))
    print(f"[cards] {len(cards)} cards -> {cards_path.relative_to(REPO_ROOT)} "
          f"({cards_path.stat().st_size} bytes)")

    for name in STATIC_ASSETS:
        src = SRC_DIR / name
        if not src.exists():
            print(f"[warn]  missing {src.relative_to(REPO_ROOT)} (skipped)",
                  file=sys.stderr)
            continue
        dst = DIST_DIR / name
        shutil.copy2(src, dst)
        print(f"[copy]  {src.relative_to(REPO_ROOT)} -> {dst.relative_to(REPO_ROOT)} "
              f"({dst.stat().st_size} bytes)")


def cache_version() -> str:
    """A short hash of the bundled assets, used by the service worker to bust
    its cache when content changes. Hashing dist/ contents means the SW reads
    a stable identifier that only changes when the build output changes."""
    h = hashlib.sha256()
    for name in ("cards.json",) + STATIC_ASSETS:
        p = DIST_DIR / name
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:12]


def stamp_service_worker(version: str) -> None:
    """Replace the placeholder cache version in the copied service worker so
    it differs across builds without us editing the source by hand."""
    sw = DIST_DIR / "service-worker.js"
    if not sw.exists():
        return
    text = sw.read_text()
    stamped = text.replace("__CACHE_VERSION__", version)
    sw.write_text(stamped)
    print(f"[stamp] service-worker.js cache version = {version}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Ship only status:'verified' or 'active' cards. "
             "Default includes drafts too while the deck is in rapid iteration.",
    )
    args = parser.parse_args()

    if not SRC_DIR.exists():
        print(f"error: {SRC_DIR} not found", file=sys.stderr)
        return 1

    cards = load_cards(include_drafts=not args.strict)
    if not cards:
        print("error: no cards loaded", file=sys.stderr)
        return 1

    write_dist(cards)
    stamp_service_worker(cache_version())
    print(f"\nbuild complete: {len(cards)} cards in {DIST_DIR.relative_to(REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
