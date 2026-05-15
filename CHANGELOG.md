# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository skeleton
- Card schema (`cards/schema.json`) with `verbatim` and `paraphrased` answer types
- Verification protocol (`AGENTS.md`) &mdash; NIST verbatim text is the source of truth
- UX principles (`docs/ux-principles.md`) &mdash; product rules, performance budgets, and architecture commitments locked in before any UI work begins
- Vulnerability disclosure policy (`SECURITY.md`)
- Strict security-header configuration (`netlify.toml`)
- Pre-commit hooks: `gitleaks` for secret scanning, basic hygiene checks
- MIT license for code, CC0 1.0 Universal for deck content
- Planning docs preserved under `docs/planning/`
- NIST SP 1308 (CSF 2.0 Quick-Start Guide) as first source PDF
- `scripts/extract.py` &mdash; Marker-based PDF-to-Markdown extraction pipeline
- First extraction landed: `sources/extracted/NIST.SP.1308/NIST.SP.1308.md` plus `sha256sum`-compatible hash
- `AGENTS.md` clarifies that `source_doc` must point to the originating document, not a navigator/QSG that re-quotes a definition
- NIST SP 800-12 Rev 1 (An Introduction to Information Security) added as canonical source
- `scripts/verify.py` &mdash; stdlib-only card verifier (schema, hash provenance, verbatim substring match, byte-equal `back == source_excerpt`)
- Pilot batch: 8 Domain 1 cards drawn from SP 800-12 section 1.4 (Information, Information Security, Confidentiality, Integrity, Data Integrity, System Integrity, Availability, Security Controls). 7 verified verbatim; Confidentiality marked `paraphrased` because a footnote splits the definition across two paragraphs in the source.
- `cards/README.md` and updated `scripts/README.md` documenting the card layout and verifier usage
- Pilot scale-up: 15 more verbatim cards from SP 800-12 sections 4 (Threats) and 5 (Policy):
  - **Policy & governance:** Information Security Policy, Procedures, Standards
  - **Risk fundamentals:** Vulnerability, Threat Source, Threat Event
  - **Threats & malware:** Malicious Hacker, Malicious Code, Virus, Trojan Horse, Worm, Logic Bomb, Ransomware, Social Engineering, Advanced Persistent Threat
- Deck stands at 23 cards: 22 verbatim-verified, 1 paraphrased awaiting human PR review
- All five remaining planned NIST sources added and extracted:
  - **NIST CSWP 29** &mdash; The NIST Cybersecurity Framework (CSF) 2.0 (81KB MD)
  - **NIST SP 800-27 Rev A** &mdash; Engineering Principles for IT Security (withdrawn by NIST but cited by ISC2) (81KB MD)
  - **NIST SP 800-34 Rev 1** &mdash; Contingency Planning Guide (423KB MD)
  - **NIST SP 800-53 Rev 5** &mdash; Security and Privacy Controls (1.8MB MD)
  - **NIST SP 800-61 Rev 2** &mdash; Computer Security Incident Handling Guide (246KB MD)
