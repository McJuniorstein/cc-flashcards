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
- 29 more cards drafted spanning four sources:
  - **From SP 800-27 Rev A (10 cards, Domains 1, 3, 4):** Access Control, Accountability, Assurance, Authentication, Authorization, Denial of Service, Identity, Risk Management (paraphrased &mdash; extraction silently dropped a hyphen), Security Policy, Threat
  - **From SP 800-34 Rev 1 (10 cards, Domain 2):** Resilience, BCP, COOP Plan, Cyber Incident Response Plan, DRP, ISCP, OEP, MTD, RTO, RPO
  - **From SP 800-61 Rev 2 (3 cards, Domain 2):** Event, Adverse Event, Computer Security Incident
  - **From CSF 2.0 / CSWP 29 (6 cards, Domain 1):** the six CSF Functions &mdash; GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER
- `scripts/verify.py` gained a normalization layer for Marker extraction artifacts: footnote markers (`<sup>N</sup>`), page-anchor spans, footnote-ref markdown links (`[N](#page-X)`), bold/italic emphasis around terms, and PDF line-break hyphenation (`word-\n\nword` &rarr; `word-word`). Applied only to the substring-in-extract check; `back == source_excerpt` stays strict.
- `AGENTS.md` updated to document the normalization step
- Deck stands at 52 cards: 50 verbatim-verified, 2 paraphrased awaiting human PR review (Confidentiality, Risk Management)

### Changed
- **Protocol bump 1.0 &rarr; 1.1 (2026-05-18):** source attribution now records the chain of provenance you actually traversed. `source_doc` is the publication you read and hashed; the rest of the chain back to the originating document goes in a new optional `source_chain` array. Replaces the prior "attribute to the originating document, not the navigator" rule, which forced fetching originating PDFs before filing cards even when the navigator already quoted them verbatim. Driven by issue #3; surfaced on PR #1 (Confidentiality is footnoted as retrieved from CNSSI 4009, which isn't in `/sources/`).
- `cards/schema.json`: added optional `source_chain` (array of unique non-empty strings, default `[]`).
- `AGENTS.md`: replaced "Attribute to the originating document, not the navigator" with "Record the source-attribution chain".
- `scripts/verify.py`: validates the shape of `source_chain` when present (array of unique non-empty strings). Does not enforce that a chain be recorded &mdash; spotting unrecorded attributions stays a human-review job.
- Re-verified all 52 cards under v1.1; no card data changes were required by this policy bump.
- **D3 batch from SP 800-53 Rev 5 glossary (8 verbatim, all promoted):** Least Privilege, Mandatory Access Control, Logical Access Control System, Physical Access Control System, Identifier, Subject, Object, Security Domain. `source_chain` populated where the 800-53r5 glossary cites another publication (CNSSI 4009, SP 800-116, FIPS 201-2). First batch drawn from the previously untapped 800-53r5 source. Deck went from 52 to 60 cards.
- **CNSSI 4009 (April 6, 2015) added as a non-NIST source.** US Government work, public domain. Used because NIST glossaries are thin on access-control and networking primitives the CC exam expects (D4 and parts of D3). Downloaded from rmf.org mirror (cnss.gov landing page is non-direct). Extracted with `scripts/extract.py`; 378KB markdown, hash `sha256:666c24d6...`.
- **800-53r5 extraction repaired:** Marker had dropped a hyphen across a line break in the Discretionary Access Control glossary entry, producing `"newlycreated"` where the PDF reads `"newly-created"`. Fixed in place; `sources/extracted/NIST.SP.800-53r5/NIST.SP.800-53r5.sha256` recomputed; the 8 D3 cards from the prior batch had their `source_hash` updated to match. All cards re-verified post-fix.
- **D3 + D4 gaps fill (15 draft cards, status: draft, awaiting PR review):**
  - D3 from CNSSI 4009: Discretionary Access Control (DAC, paraphrased), Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), Privileged Account, Privileged User, Need-to-Know (paraphrased). `source_chain` populated where CNSSI cites NIST SP 800-53 Rev 4, E.O. 13526, etc. — Rev 4 kept literal per v1.1 historical-provenance rule, despite Rev 5 being current-effective.
  - D3 from 800-53r5 AC-5 Discussion: Separation of Duties (paraphrased).
  - D4 from CNSSI 4009: Firewall, Demilitarized Zone (DMZ), Virtual Private Network (VPN, paraphrased), Intrusion Detection System (IDS, paraphrased), Intrusion Prevention System (IPS), Man-in-the-Middle Attack (MITM).
  - D4 stretch (flagged in PR for reviewer decision): OSI Model and TCP/IP Model. CNSSI 4009 only contains the acronym expansions; the layer counts are textbook knowledge not present in our source corpus. Filed paraphrased with `source_chain` pointing at ISO/IEC 7498-1 and IETF RFC 1122 respectively.
  - Staging file at `cards/drafts/2026-05-18_D3-D4-gaps.md` records the rationale, source_excerpts, and flags for PR review.
- Deck stands at 75 cards: 60 verified (58 verbatim + 2 paraphrased pre-existing), 15 draft (7 verbatim + 8 paraphrased — pending PR review).
- Domain coverage shift: D1=25, D2=13, **D3=19 (+7 this session, +8 from PR #8)**, **D4=9 (+8 this session, was 1)**, D5=9. D4 is no longer single-digit-card thin.

### Known gaps still open
- **Rule-Based Access Control** — not defined in CNSSI 4009 or any existing source.
- **Packet, Frame, Port (as networking concepts)** — only compound terms exist in CNSSI 4009. NIST SP 800-94 / RFC-level source addition would unblock.
- **VLAN, Network Segmentation** — not in CNSSI 4009. Likely covered by NIST SP 800-125B or 800-41.
- **D5 still light** — 9 cards covers Sec Ops thinly. SP 800-53 Rev 5 AU/CM/IR/SI families are untapped.
- **OSI Model / TCP/IP Model** — filed but flagged; awaiting reviewer decision on the provenance stretch.
