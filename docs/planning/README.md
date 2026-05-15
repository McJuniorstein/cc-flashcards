# Planning documents

These are historical planning artefacts kept for context and for the project's development arc. **The canonical, current state of the project lives in [`/AGENTS.md`](../../AGENTS.md) and the top-level [`README.md`](../../README.md).** If anything here conflicts with those, those win.

## Contents

- `14may26_2030_cc_flashcards_plan_v3.md` &mdash; original V3 planning doc (pre-discussion).
- `possible_planning_addendum.md` &mdash; critique that surfaced schema and provenance issues addressed in the final design.

## Notable evolution between planning and current design

The biggest shift from V3: the multi-model verification protocol was simplified once the project committed to **verbatim NIST quoting** as the default for cards. With verbatim text, verification reduces to a string-equality check against extracted source text, not a semantic judgement across multiple models. Multi-model review remains an option for the small subset of cards that genuinely require paraphrase, but is not the primary mechanism.

See [`/AGENTS.md`](../../AGENTS.md) for the current verification protocol.
