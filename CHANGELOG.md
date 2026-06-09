# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `scripts/test_verify.py` &mdash; stdlib `unittest` suite for `verify.py` (the protocol guardian): 42 tests covering the normalization layer (every Marker artifact + whitespace), full schema validation (including `source_chain` shape), and the `verify_card` ok/paraphrased/fail paths exercised against real temp files (verbatim match, byte-mismatch, excerpt-not-found, normalization-only match, hash-mismatch-on-disk, unknown hash, invalid JSON) plus `load_known_sources`. No new dependencies; run with `python3 scripts/test_verify.py`. Documented in `scripts/README.md`.
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
- **Post-PR-#9 promotion (2026-05-18):** all 15 PR-#9 drafts promoted from `status: "draft"` to `"verified"`. Verbatim cards via `scripts/verify.py --promote`; paraphrased cards (DAC, Need-to-Know, Separation of Duties, VPN, IDS, OSI Model, TCP/IP Model) flipped manually with `modified_at` set, since the human PR review required by AGENTS.md happened on PR #9. The OSI and TCP/IP cards keep their ⚠ provenance-stretch flags documented in the staging file `cards/drafts/2026-05-18_D3-D4-gaps.md`. Deck moved to 75 verified / 0 draft.
- **D4 + D5 batch from CNSSI 4009 (16 draft cards, status: draft, awaiting PR review):**
  - D4 (8): Distributed Denial of Service (DDoS), Packet Sniffer, Wireless Access Point (WAP), Wi-Fi Protected Access 2 (WPA2, paraphrased), Jamming, Wireless Intrusion Detection System (WIDS), Gateway, Proxy. `source_chain` populated for Jamming (IETF RFC 4949 Ver 2), WIDS (DoD 8420.1), Gateway (IETF RFC 4949 Ver 2), Proxy (NIST SP 800-44 Rev 2); others organic to CNSSI.
  - D5 (8): Encryption, Hashing, Symmetric Encryption Algorithm, Public Key Cryptography (PKC), Baseline Configuration, Configuration Management (paraphrased), Patch Management, Security Awareness and Training Program. `source_chain` populated for Encryption (ISO/IEC 7498-2), Hashing (NIST SP 800-72), Symmetric Encryption Algorithm (NIST SP 800-49), Baseline Configuration and Configuration Management (NIST SP 800-53 Rev 4); others organic to CNSSI.
  - 14 verbatim + 2 paraphrased (WPA2 and Configuration Management shortened for flashcard readability; original CNSSI text preserved in `source_excerpt`).
  - Staging file at `cards/drafts/2026-05-18_D4-D5-batch.md` records the full content and the deferred-gaps section.
- Deck stands at **91 cards**: 75 verified (after PR-#9 promotion) + 16 draft (this batch). Verbatim ratio: 80/91 = 88%.
- Domain coverage shift: D1=25, D2=13, D3=19, **D4=17 (+8 this session, was 9)**, **D5=17 (+8 this session, was 9)**. Deck distribution now within 5 points of exam weighting in every domain.

### Known gaps still open after the D4+D5 batch
- **Carried forward from PR #9:** Rule-Based Access Control (no NIST/CNSSI source).
- **D4 carried forward:** Packet, Frame, Segment/Datagram, Port (well-known/registered/dynamic), IPv4, IPv6, ARP, VLAN, Network Segmentation. None are standalone glossary entries in CNSSI 4009 or any existing source; would need RFC 1122 / NIST SP 800-94 / 800-41 / 800-125B added.
- **D5 carried forward:** Data Classification, System Hardening, Acceptable Use Policy (AUP). Not in CNSSI 4009 as standalone entries.
- **OSI Model / TCP/IP Model** flags retained in staging file `cards/drafts/2026-05-18_D3-D4-gaps.md` even after promotion. Reviewer's call to keep stands.
- **Post-PR-#10 promotion (2026-05-18):** all 16 PR-#10 drafts promoted to `status: "verified"`. 14 verbatim via `verify.py --promote`; 2 paraphrased (WPA2, Configuration Management) flipped manually since human review happened on PR #10. Deck moved to 91 verified / 0 draft.
- **Three new sources added (2026-05-18):**
  - **NIST SP 800-94** (Guide to Intrusion Detection and Prevention Systems, 2007) &mdash; downloaded from nvlpubs.nist.gov, 1.1MB PDF, 385KB extracted MD, hash `sha256:4562ebba...`. Unlocks IDPS depth (anomaly vs signature detection, false positives/negatives, HIDS/HIPS, NIDS/NIPS).
  - **NIST SP 800-41 Rev 1** (Guidelines on Firewalls and Firewall Policy, September 2009) &mdash; nvlpubs.nist.gov, 332KB PDF, 141KB extracted MD, hash `sha256:46fc63d5...`. Unlocks firewall depth (packet filter, stateful inspection, NAT, application-proxy gateway, egress/ingress filtering, deny by default).
  - **IETF RFC 4949** (Internet Security Glossary v2, August 2007) &mdash; rfc-editor.org PDF rendering, 547KB PDF, 725KB extracted MD, hash `sha256:7b42adb9...`. First IETF source in the corpus. Already cited as the chain source for several existing cards (Jamming, Gateway, MITM); provides authoritative glossary entries for Packet, Datagram, UDP.
- **D4 primitives + depth batch (16 draft cards, status: draft, awaiting PR review):**
  - From RFC 4949 (3): Packet, Datagram (paraphrased &mdash; editorial brackets dropped), UDP (paraphrased &mdash; RFC ref dropped). Datagram's `source_chain` records IETF RFC 1983 (quoted source); UDP's records IETF RFC 768.
  - From SP 800-94 (6): Anomaly-Based Detection, Signature-Based Detection, False Positive, False Negative, HIDS/HIPS, NIDS/NIPS. All organic to 800-94 (empty chain).
  - From SP 800-41 Rev 1 (7): Packet Filter, Stateful Inspection, NAT, Application-Proxy Gateway, Egress Filtering, Ingress Filtering, Deny by Default. All organic to 800-41r1.
  - 14 verbatim + 2 paraphrased. Staging file at `cards/drafts/2026-05-18_D4-primitives-batch.md`.
- Deck stands at **107 cards**: 91 verified (after PR-#10 promotion) + 16 draft (this batch). Verbatim ratio: 94/107 = 88%.
- Domain coverage shift: D1=25, D2=13, D3=19, **D4=33 (+16 this session, was 17)**, D5=17. D4 is now over-represented (31% deck vs 24% exam) &mdash; an over-correction from being severely under at 1%. Future batches should skew D1/D3/D5.

### Known gaps still open after the D4 primitives batch
- **Frame, Port (well-known/registered/dynamic), IPv4, IPv6, ARP, VLAN, Network Segmentation** &mdash; surveyed all three new sources, none have these as standalone glossary entries. Would need RFC 826 (ARP), RFC 8200 (IPv6), IEEE 802.1Q or NIST SP 800-125B (VLAN), or RFC 1180 / NIST SP 800-115 (port classifications).
- **Network Segmentation** surprisingly absent from 800-41r1 narrative as well as glossary.
- **Rule-Based Access Control** &mdash; still no clean source.
- **D5 expansion** &mdash; 17 cards is in-range for exam weight but additional batches could draw from 800-53r5 AU/CM/IR/SI families.
- **D3 slightly under exam weight** (18% deck vs 22% exam). A small follow-on D3 batch would help.
- **Post-PR-#11 promotion (2026-05-19):** all 16 PR-#11 drafts promoted to `status: "verified"`. 14 verbatim via `verify.py --promote`; 2 paraphrased (Datagram, UDP) flipped manually. Deck moved to 107 verified / 0 draft.
- **Final light batch (9 draft cards, status: draft, awaiting PR review):**
  - D3 (2 verbatim): Access Enforcement (from 800-53r5 AC-3 Control statement), Identification (from CNSSI 4009, chain: FIPS PUB 201-1).
  - D4 (1 verbatim + 1 paraphrased): External Network (from 800-53r5 glossary), Internal Network (paraphrased — shortened from 800-53r5 glossary).
  - D5 (5 verbatim): Audit Log (chain: NIST SP 800-53 Rev 4), Audit Record (chain: NIST SP 800-53 Rev 4), Audit Trail (chain: NIST SP 800-47), Vulnerability Assessment (from CNSSI 4009), Continuous Monitoring (chain: NIST SP 800-137).
  - 8 verbatim + 1 paraphrased. All from already-extracted sources; no new source PDFs added. Staging file at `cards/drafts/2026-05-19_Final-Light-Batch.md`.
- Deck stands at **116 cards**: 107 verified (after PR-#11 promotion) + 9 draft (this batch). Verbatim ratio: 102/116 = 88%.
- Domain coverage shift: D1=25, D2=13, **D3=21 (+2)**, **D4=35 (+2)**, **D5=22 (+5)**. Lands inside the planned 110-130 "worthwhile study pack" range.
- **Content phase complete. Next phase: minimal static app (HTML + vanilla JS + Tailwind) per `docs/ux-principles.md`.**
- **V1 static app skeleton (2026-05-19):** built per `docs/ux-principles.md`. Files at `app/src/{index.html, app.js, style.css, service-worker.js}`; build pipeline at `scripts/build_app.py` reads `cards/cc-*.json`, filters to non-deprecated, writes `app/dist/cards.json` + copies static assets. `netlify.toml` build command updated from placeholder to `python3 scripts/build_app.py`.
  - **No CSS framework.** Tailwind CDN was rejected: it requires inline scripts/styles (CSP-blocked by the existing `netlify.toml`), ships ~340KB JS (blows the 50KB ceiling), and violates the "no third-party JS on the critical path" rule. Vanilla CSS at ~2.4KB gzipped fits the 10KB target with room to spare.
  - **Three views**: setup (pick mode), study (card front/back + mark), done (session summary). Implemented as `hidden`-toggled `<section>` elements; no router.
  - **Interactions** (per ux-principles "Interaction model (locked)"): tap/space/enter to flip; K = known; R = review again; Escape = end session.
  - **State**: `localStorage` for known + review sets and theme preference. No server. No accounts.
  - **Service worker**: cache-first for shell, stale-while-revalidate for `cards.json`. Cache version is a build-time hash so deploys evict stale entries.
  - **Theme**: auto (follows `prefers-color-scheme`) / light / dark. Toggle persists.
  - **Accessibility**: skip link, semantic landmarks, `aria-live` for state changes, focus management on view switches, `prefers-reduced-motion` respected. Lighthouse Accessibility 100 (headless, dev server).
  - **Bundle sizes (gzipped)**: HTML 1.5KB, JS 3.4KB, CSS 2.4KB, service worker 0.9KB, cards.json 10.1KB. All shell assets well under their `docs/ux-principles.md` budgets (HTML target <15KB, JS <30KB, CSS <10KB).
  - **Lighthouse scores (local headless, dev server)**: Performance 98, Accessibility 100, Best Practices 100, SEO 100. The 3 deductions in Performance sub-audits (cache headers, document latency, JS minification) are dev-server artifacts — Netlify will resolve them in production via Brotli + immutable headers.

### Known gaps still open after the final light batch
- **D3 still under exam weight** (18% deck vs 22% exam). A 4-5 card follow-on batch could close it; not blocking app work.
- **D4 over by 6 points** &mdash; overcorrection from starting at 1%. Future batches should NOT add D4.
- **Carried-forward primitives** (Frame, Port classifications, IPv4, IPv6, ARP, VLAN, Network Segmentation, Rule-Based AC, Data Classification, AUP, Hardening) &mdash; still no clean source. Addressed if/when new sources are added post-app.
