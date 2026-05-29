# Re-sourcing the OSI / TCP-IP model cards (2026-05-29)

Audit record for reconciling the two model cards (`cc-aaaa0001`, `cc-aaaa0002`)
with the `paraphrased` rules in `AGENTS.md`. These were the deck's weakest cards:
their `source_excerpt` was only the CNSSI 4009 acronym expansion, while the `back`
asserted layer counts, layer names, and standards references that appear nowhere
in that excerpt — and chained to documents (`ISO/IEC 7498-1`, `IETF RFC 1122`)
that are **not** in `/sources/`. The TCP/IP card additionally asserted "four-layer,"
which is unsupported by — and inconsistent with — the only held source that
addresses the model.

**Fix:** re-source both cards to `IETF RFC 4949`
(`sha256:7b42adb9c4c8a15aca42d338ec92edae59151004db21510f88e609fea9e53807`), which
is already in `/sources/` and hashed, and which actually defines both models in its
glossary. Each `source_excerpt` below is a verified verbatim substring of the RFC
4949 extraction.

## cc-aaaa0001 — OSI Model

- **source_doc:** `CNSSI 4009` → `IETF RFC 4949`
- **source_section:** `Annex A — Acronyms` → `Glossary — Open Systems Interconnection (OSI) Reference Model (OSIRM)`
- **source_chain:** `["ISO/IEC 7498-1"]` (unchanged — RFC 4949 cites `[I7498-1]`)
- **source_excerpt:** *"Open Systems Interconnection (OSI) Reference Model (OSIRM) (N) A joint ISO/ITU-T standard [I7498-1] for a seven-layer, architectural communication framework for interconnection of computers in networks."*
- **back:** *"A joint ISO/ITU-T standard (ISO/IEC 7498-1) defining a seven-layer architectural framework for network communication: Physical, Data Link, Network, Transport, Session, Presentation, and Application."*

Rule check: "joint ISO/ITU-T standard," "ISO/IEC 7498-1" (`[I7498-1]`), "seven-layer,"
and "framework for network communication" are all in the excerpt. The seven layer
**names** are not in this excerpt sentence but are verbatim in the same source's
OSIRM/IPS layer-alignment diagram (`7.Application … 1.Physical`), so no information
in the `back` originates outside RFC 4949. Retaining the names was an explicit
editorial decision (study value); the derivation is approved per the human-review
clause in `AGENTS.md`.

## cc-aaaa0002 — TCP/IP Model

- **source_doc:** `CNSSI 4009` → `IETF RFC 4949`
- **source_section:** `Annex A — Acronyms` → `Glossary — Internet Protocol Suite (IPS)`
- **source_chain:** `["IETF RFC 1122"]` → `[]` (RFC 1122 is not held; the five-layer treatment is RFC 4949's own, so there is no upstream document to chain to)
- **source_excerpt:** *"This Glossary treats the IPS as having five protocol layers -- Application, Transport, Internet, Network Interface, and Network Hardware"*
- **back:** *"The IETF Internet Protocol Suite (TCP/IP), which RFC 4949 treats as five layers: Application, Transport, Internet, Network Interface, and Network Hardware. It has no distinct Session or Presentation layer; those OSI upper-layer functions fold into the application."*

Rule check: the five-layer enumeration is verbatim in the excerpt. The phrase
*"It has no distinct Session or Presentation layer"* paraphrases RFC 4949's
*"the IPS model does not include Session and Presentation layers"* (same source).
The card is now **attributed** ("which RFC 4949 treats as five layers") rather than
asserting a layer count as universal fact — important because the commonly taught
four-layer RFC 1122 model differs, and RFC 1122 is not in the corpus. If the
four-layer framing is wanted later, the correct path is to add RFC 1122 to
`/sources/`, extract + hash it, and source a separate card from it.

Both cards remain `answer_type: paraphrased`, `status: verified`. `modified_at`
bumped to `2026-05-29T04:07:35Z`.
