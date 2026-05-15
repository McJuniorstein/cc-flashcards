# Sources

This directory holds the authoritative source documents that every card cites.

## Layout

- `*.pdf` &mdash; original NIST publications, downloaded directly from nist.gov
- `extracted/*.md` &mdash; Markdown extraction (via [Marker](https://github.com/VikParuchuri/marker)) for use by the verification pipeline
- `extracted/*.sha256` &mdash; SHA-256 hash of each extracted file, referenced by `source_hash` in card records

## Documents

> _One row per source. Includes the download URL and date for reproducibility._

| Identifier | Title | Source URL | Downloaded |
|---|---|---|---|
| NIST SP 1308 | NIST Cybersecurity Framework 2.0: Cybersecurity, Enterprise Risk Management, and Workforce Management Quick-Start Guide | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1308.pdf | 2026-05-15 |
| NIST SP 800-12 Rev 1 | An Introduction to Information Security | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-12r1.pdf | 2026-05-15 |

Still to add (per `docs/planning/`):

- NIST CSF 2.0 (the framework itself; SP 1308 above is the companion Quick-Start Guide)
- NIST SP 800-27 Rev A (withdrawn by NIST but still cited by ISC2)
- NIST SP 800-53 Rev 5
- NIST SP 800-61 Rev 2
- NIST SP 800-34

## Reproducing the source set

1. Download the listed PDFs from the URLs above into this directory.
2. Run `scripts/extract.py` (not yet implemented) to produce the Markdown extractions and SHA-256 hashes under `extracted/`.
3. The extracted Markdown is what every card's `source_excerpt` is drawn from.

## Why PDFs live in the repo

NIST publications are US government works in the public domain. Versioning them alongside the deck means:

- Anyone cloning the repo can reproduce verification end-to-end
- Source changes (NIST republishes a document) are visible via git history
- The `source_hash` per card detects silent drift even if a PDF is replaced
