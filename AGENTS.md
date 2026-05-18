# AGENTS.md &mdash; Verification Protocol

This document is the contract that any agent &mdash; human or AI &mdash; works against when contributing cards to this project. It is intentionally short and prescriptive.

**Protocol version:** 1.1 (2026-05-18)

---

## Core rule

**NIST verbiage is the final say.** When NIST defines a term in a cited publication, that exact text is what goes on the card. We do not interpret, summarize, simplify, or teach. We quote and we cite.

## Card lifecycle

```
draft  ->  verified  ->  active  ->  (deprecated)
```

- **draft**: card has been written but not yet verified
- **verified**: card has passed every check below
- **active**: card is published in the deck
- **deprecated**: card is retained for historical reasoning but no longer shown

Cards are never deleted. State changes are recorded via `modified_at`.

## Two answer types

Every card declares its `answer_type`.

### `verbatim` (preferred &mdash; target >=90% of cards)

- `back` is **byte-identical** to `source_excerpt`
- `source_excerpt` is the clean human-readable definition text as it appears in the extracted source document, with Marker's extraction artifacts (footnote markers, page-anchor spans, markdown emphasis around terms) removed
- The verifier checks (a) that `source_excerpt` appears as a substring of the extracted Markdown **after normalizing those same artifacts on both sides**, and (b) that `back == source_excerpt` byte-for-byte. Normalization applies only to the substring search; `back == source_excerpt` stays strict.
- No model judgement involved.

### `paraphrased` (exception &mdash; minimise)

Allowed only when:
- The source definition spans multiple non-contiguous passages and must be assembled
- The source definition is too long to fit on a card and must be condensed without changing meaning
- The CC outline references a concept that has no clean NIST definition available

Rules for paraphrased cards:
- `source_excerpt` still contains the verbatim source text the paraphrase is derived from
- The paraphrase must not add information not present in the excerpt
- The paraphrase must not change normative language (e.g., "shall" vs "should" vs "may")
- The paraphrase must preserve precise terminology: `authorization` is not `authentication`; `integrity` is not `availability`
- Every paraphrased card requires human review before promotion to `verified`

## Verification checklist (per card)

A card moves from `draft` to `verified` only when **all** are true:

1. **Source match**
   - `verbatim`: `back` == `source_excerpt` (exact)
   - `paraphrased`: human review approves the derivation
2. **Citation accuracy**: `source_doc` (and `source_section` if specified) correctly identify where `source_excerpt` came from
3. **Source freshness**: `source_hash` matches the current SHA-256 of the extracted source document
4. **Domain assignment**: `primary_domain` is one of 1&ndash;5 and reflects ISC2 CC exam-outline placement
5. **No duplicates**: no other card shares the same `front` term and no other card has a semantically equivalent `back`
6. **Front is unambiguous**: the term on the front has a single correct definition in the deck

## Review surface

When a `paraphrased` card is drafted, or when the programmatic verbatim check fails:

- Open a GitHub PR for that card
- PR body includes: the card JSON, the source excerpt, the diff (for verbatim mismatches), the reasoning for any paraphrase choice
- A human reviewer approves or requests changes
- Approved PRs merge the card with `status: verified`

This gives the project a permanent, public audit trail of every editorial decision.

## Source citation rules

- Use the exact NIST identifier, e.g., `NIST SP 800-12 Rev 1`, `NIST SP 800-53 Rev 5`, `NIST CSF 2.0`
- For withdrawn NIST publications still cited by ISC2 (notably `SP 800-27 Rev A`): cite them the way ISC2 does. Do not editorialise about withdrawal status.
- `source_section` is optional but encouraged when the source has clear section structure (e.g., `Section 2.3`)

### Record the source-attribution chain

`source_doc` is the publication you actually read and hashed &mdash; the document from `/sources/extracted/` that the definition was lifted from. When that document attributes the definition to another publication (a footnote, an inline citation), record the rest of the chain in `source_chain`, ordered from closest to originating.

Example: SP 800-12r1's definition of Confidentiality is footnoted *"retrieved from CNSSI 4009"*. The card records `source_doc: "NIST SP 800-12 Rev 1"` and `source_chain: ["CNSSI 4009"]`.

If the chain stacks (navigator A cites navigator B cites originating C), record all of it: `source_chain: ["B", "C"]`. The full provenance chain is therefore `[source_doc, ...source_chain]`; the first element is what you read, the last is the originating document.

`source_hash` and `source_section` stay attached to `source_doc` &mdash; the document you actually read and hashed. Chain entries are bibliographic strings only; they do not need to exist in `/sources/`.

The verifier validates the *shape* of `source_chain` (array of unique non-empty strings) but does not enforce that a chain be recorded; spotting unrecorded attributions is a human-review responsibility for now.

## Out of scope for this protocol

- Teaching the material. Explanations belong in user-facing UI text and the README, not on cards.
- Generating exam questions. Cards are term/definition pairs, not Q&A.
- Paraphrasing for clarity. If a definition is unclear, that is a NIST critique, not a license to rewrite.

## Updates to this document

Changes to `AGENTS.md` are themselves a verification event: every existing `verified` card must be re-checked against the new protocol. Bump the protocol version and record the change in `CHANGELOG.md`.
