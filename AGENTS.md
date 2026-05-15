# AGENTS.md &mdash; Verification Protocol

This document is the contract that any agent &mdash; human or AI &mdash; works against when contributing cards to this project. It is intentionally short and prescriptive.

**Protocol version:** 1.0 (2026-05-15)

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
- `source_excerpt` is pulled directly from the extracted source document
- Verification is a string equality check plus a source-hash match. No model judgement involved.

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

### Attribute to the originating document, not the navigator

NIST publications &mdash; especially Quick-Start Guides (QSGs) and Frameworks &mdash; routinely re-quote definitions from other NIST publications. For example, SP 1308 lists "High Value Asset" in its Key Terms but the canonical definition lives in `NIST SP 800-160 Vol. 2 Rev. 1`. A card's `source_doc` field must always point to the **originating** document the definition was written for, not the navigator document that happens to surface it.

If you encounter a definition in a navigator document and the originating document is not yet in `/sources/`, do one of two things:

1. Download the originating document, add it to `/sources/`, run `scripts/extract.py`, and cite the originating extraction.
2. Skip the card for now and add the originating document to `/sources/README.md`'s "still to add" list.

Never cite the navigator just because that's where you read the definition.

## Out of scope for this protocol

- Teaching the material. Explanations belong in user-facing UI text and the README, not on cards.
- Generating exam questions. Cards are term/definition pairs, not Q&A.
- Paraphrasing for clarity. If a definition is unclear, that is a NIST critique, not a license to rewrite.

## Updates to this document

Changes to `AGENTS.md` are themselves a verification event: every existing `verified` card must be re-checked against the new protocol. Bump the protocol version and record the change in `CHANGELOG.md`.
