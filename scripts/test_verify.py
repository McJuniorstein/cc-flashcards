#!/usr/bin/env python3
"""Unit tests for scripts/verify.py — the guardian of the card protocol.

Stdlib-only (unittest), matching the project's no-dependencies stance. Run:

    python3 -m unittest scripts.test_verify        # from repo root
    python3 scripts/test_verify.py                 # direct

The suite covers the three pieces verify.py owns:
  - normalize_for_substring_check: each Marker artifact + whitespace
  - validate_schema: every field rule, including source_chain shape
  - verify_card: the verbatim / paraphrased / failure paths, exercised
    against real temp files so the hashing and substring logic run for real.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

# verify.py lives next to this file and is not packaged; import it directly.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify  # noqa: E402


def _valid_card(**overrides) -> dict:
    """A schema-valid card; override individual fields per test."""
    card = {
        "id": "cc-abc123",
        "front": "Term",
        "back": "A definition.",
        "source_doc": "NIST SP 800-12 Rev 1",
        "source_section": "Section 1.4",
        "source_chain": [],
        "source_excerpt": "A definition.",
        "source_hash": "sha256:" + "a" * 64,
        "answer_type": "verbatim",
        "primary_domain": 1,
        "secondary_domains": [],
        "status": "verified",
        "created_at": "2026-05-18T22:47:23Z",
        "modified_at": None,
    }
    card.update(overrides)
    return card


class NormalizeTests(unittest.TestCase):
    """normalize_for_substring_check strips deterministic Marker artifacts."""

    def n(self, text: str) -> str:
        return verify.normalize_for_substring_check(text)

    def test_strips_sup_footnote_markers(self):
        self.assertEqual(self.n("integrity<sup>3</sup> of data"), "integrity of data")

    def test_strips_page_anchor_spans(self):
        self.assertEqual(
            self.n('the <span id="page-8-1"></span>process'), "the process"
        )

    def test_strips_footnote_reference_links(self):
        self.assertEqual(self.n("incidents[1](#page-8-2) are"), "incidents are")

    def test_unwraps_bold(self):
        self.assertEqual(self.n("**Confidentiality** means"), "Confidentiality means")

    def test_unwraps_italic(self):
        self.assertEqual(self.n("an *intrusion detection system*"),
                         "an intrusion detection system")

    def test_rejoins_hyphen_break(self):
        # PDF wrapped "newly-created" across a blank line.
        self.assertEqual(self.n("newly-\n\ncreated objects"), "newly-created objects")

    def test_collapses_whitespace(self):
        self.assertEqual(self.n("a   b\n\tc"), "a b c")

    def test_strips_leading_and_trailing_whitespace(self):
        self.assertEqual(self.n("  padded  "), "padded")

    def test_does_not_join_spaced_hyphen(self):
        # A hyphen NOT preceded by a word char (e.g. a dash or list marker) must
        # not be glued to the following word.
        self.assertEqual(self.n("section - title"), "section - title")

    def test_combination_of_artifacts(self):
        raw = "**Integrity**<sup>2</sup> guards *data*[3](#page-1-2) end-\n\nto-end"
        self.assertEqual(self.n(raw), "Integrity guards data end-to-end")

    def test_byte_strictness_is_independent(self):
        # Normalization is only for the substring check; it must not be used to
        # judge back==excerpt. Two strings that normalize equal are still
        # distinct bytes, which is what the verbatim byte-check relies on.
        a, b = "**term**", "term"
        self.assertEqual(self.n(a), self.n(b))
        self.assertNotEqual(a, b)


class ValidateSchemaTests(unittest.TestCase):
    """validate_schema raises CardError on every malformed field."""

    def check(self, card: dict, stem: str = "cc-abc123"):
        verify.validate_schema(card, Path(f"{stem}.json"))

    def assertRejects(self, card: dict, stem: str = "cc-abc123"):
        with self.assertRaises(verify.CardError):
            self.check(card, stem)

    def test_valid_card_passes(self):
        self.check(_valid_card())  # must not raise

    def test_absent_optional_fields_pass(self):
        card = _valid_card()
        del card["source_chain"]
        del card["source_hash"]
        del card["modified_at"]
        self.check(card)

    def test_missing_required_field(self):
        card = _valid_card()
        del card["back"]
        self.assertRejects(card)

    def test_wrong_type_for_primary_domain(self):
        self.assertRejects(_valid_card(primary_domain="1"))

    def test_bad_id_pattern(self):
        self.assertRejects(_valid_card(id="card-1"), stem="card-1")

    def test_id_must_match_filename_stem(self):
        self.assertRejects(_valid_card(id="cc-abc123"), stem="cc-zzz999")

    def test_invalid_answer_type(self):
        self.assertRejects(_valid_card(answer_type="quote"))

    def test_invalid_status(self):
        self.assertRejects(_valid_card(status="published"))

    def test_primary_domain_out_of_range_low(self):
        self.assertRejects(_valid_card(primary_domain=0))

    def test_primary_domain_out_of_range_high(self):
        self.assertRejects(_valid_card(primary_domain=6))

    def test_primary_domain_bounds_ok(self):
        self.check(_valid_card(primary_domain=1))
        self.check(_valid_card(primary_domain=5))

    def test_bad_source_hash_format(self):
        self.assertRejects(_valid_card(source_hash="sha256:XYZ"))
        self.assertRejects(_valid_card(source_hash="md5:" + "a" * 64))

    def test_source_hash_none_is_allowed(self):
        self.check(_valid_card(source_hash=None))

    def test_source_chain_not_a_list(self):
        self.assertRejects(_valid_card(source_chain="CNSSI 4009"))

    def test_source_chain_non_string_entry(self):
        self.assertRejects(_valid_card(source_chain=[123]))

    def test_source_chain_empty_entry(self):
        self.assertRejects(_valid_card(source_chain=[""]))

    def test_source_chain_duplicate_entry(self):
        self.assertRejects(_valid_card(source_chain=["CNSSI 4009", "CNSSI 4009"]))

    def test_source_chain_valid_passes(self):
        self.check(_valid_card(source_chain=["CNSSI 4009", "ISO/IEC 7498-1"]))


class VerifyCardTests(unittest.TestCase):
    """verify_card end-to-end against real temp source + card files."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def _write_source(self, text: str) -> tuple[Path, str, dict]:
        """Write a source .md, return (path, digest, known_sources mapping)."""
        md = self.tmp / "source.md"
        md.write_text(text)
        digest = hashlib.sha256(text.encode()).hexdigest()
        return md, digest, {digest: md}

    def _write_card(self, card: dict) -> Path:
        path = self.tmp / f"{card['id']}.json"
        path.write_text(json.dumps(card))
        return path

    def test_verbatim_match_ok(self):
        md, digest, known = self._write_source("The CIA triad: confidentiality, integrity, availability.")
        excerpt = "confidentiality, integrity, availability"
        path = self._write_card(_valid_card(
            source_excerpt=excerpt, back=excerpt, source_hash="sha256:" + digest,
        ))
        self.assertEqual(verify.verify_card(path, known)[0], "ok")

    def test_verbatim_back_differs_from_excerpt_fails(self):
        md, digest, known = self._write_source("availability is uptime")
        path = self._write_card(_valid_card(
            source_excerpt="availability is uptime",
            back="availability means uptime",  # not byte-identical
            source_hash="sha256:" + digest,
        ))
        status, msg = verify.verify_card(path, known)
        self.assertEqual(status, "fail")
        self.assertIn("byte-for-byte", msg)

    def test_verbatim_excerpt_absent_from_source_fails(self):
        md, digest, known = self._write_source("the quick brown fox")
        path = self._write_card(_valid_card(
            source_excerpt="lazy dog", back="lazy dog",
            source_hash="sha256:" + digest,
        ))
        status, msg = verify.verify_card(path, known)
        self.assertEqual(status, "fail")
        self.assertIn("not found", msg)

    def test_verbatim_match_only_after_normalization(self):
        # Source carries Marker artifacts; the clean excerpt must still match.
        md, digest, known = self._write_source("guards **data** integrity<sup>4</sup> end-\n\nto-end")
        excerpt = "guards data integrity end-to-end"
        path = self._write_card(_valid_card(
            source_excerpt=excerpt, back=excerpt, source_hash="sha256:" + digest,
        ))
        self.assertEqual(verify.verify_card(path, known)[0], "ok")

    def test_paraphrased_is_flagged_not_failed(self):
        md, digest, known = self._write_source("some source text")
        path = self._write_card(_valid_card(
            answer_type="paraphrased",
            source_excerpt="some source text",
            back="a reworded definition entirely unlike the excerpt",
            source_hash="sha256:" + digest,
        ))
        # Paraphrased path never reaches the substring/byte checks.
        self.assertEqual(verify.verify_card(path, known)[0], "paraphrased")

    def test_missing_source_hash_fails(self):
        path = self._write_card(_valid_card(source_hash=None))
        status, msg = verify.verify_card(path, {})
        self.assertEqual(status, "fail")
        self.assertIn("source_hash", msg)

    def test_unknown_hash_fails(self):
        path = self._write_card(_valid_card(source_hash="sha256:" + "b" * 64))
        status, msg = verify.verify_card(path, {})  # empty registry
        self.assertEqual(status, "fail")
        self.assertIn("no extracted source", msg)

    def test_hash_mismatch_on_disk_fails(self):
        # Registry claims digest X maps to a file, but the file's real content
        # hashes to Y — i.e. the source was mutated after the card was filed.
        md = self.tmp / "source.md"
        md.write_text("mutated content")
        claimed = "c" * 64
        known = {claimed: md}
        path = self._write_card(_valid_card(source_hash="sha256:" + claimed))
        status, msg = verify.verify_card(path, known)
        self.assertEqual(status, "fail")
        self.assertIn("hash mismatch", msg)

    def test_invalid_json_fails(self):
        path = self.tmp / "cc-broken.json"
        path.write_text("{ not valid json ")
        status, msg = verify.verify_card(path, {})
        self.assertEqual(status, "fail")
        self.assertIn("invalid JSON", msg)

    def test_schema_failure_short_circuits(self):
        path = self._write_card(_valid_card(primary_domain=9))
        status, msg = verify.verify_card(path, {})
        self.assertEqual(status, "fail")
        self.assertIn("schema", msg)


class LoadKnownSourcesTests(unittest.TestCase):
    """load_known_sources maps .sha256 digests to their sibling .md files."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self._orig = verify.EXTRACTED_DIR
        verify.EXTRACTED_DIR = self.tmp
        self.addCleanup(lambda: setattr(verify, "EXTRACTED_DIR", self._orig))

    def test_maps_digest_to_md_path(self):
        sub = self.tmp / "DOC"
        sub.mkdir()
        (sub / "DOC.md").write_text("body")
        # sha256sum-style line: "<digest>  <filename>"
        (sub / "DOC.sha256").write_text("deadbeef" + "0" * 56 + "  DOC.md\n")
        known = verify.load_known_sources()
        self.assertIn("deadbeef" + "0" * 56, known)
        self.assertEqual(known["deadbeef" + "0" * 56].name, "DOC.md")

    def test_sha256_without_sibling_md_is_skipped(self):
        sub = self.tmp / "DOC"
        sub.mkdir()
        (sub / "DOC.sha256").write_text("abc123  DOC.md\n")  # no DOC.md present
        self.assertEqual(verify.load_known_sources(), {})

    def test_empty_when_no_extracted_dir(self):
        verify.EXTRACTED_DIR = self.tmp / "does-not-exist"
        self.assertEqual(verify.load_known_sources(), {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
