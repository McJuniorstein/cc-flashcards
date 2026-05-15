# cards/

One JSON file per card, named after its `id`: `cards/<id>.json`. Schema lives in [`schema.json`](./schema.json). The verification protocol that governs cards lives in [`/AGENTS.md`](../AGENTS.md). The deck's content license is CC0 1.0 Universal &mdash; see [`LICENSE`](./LICENSE).

## Card lifecycle

```
draft  ->  verified  ->  active  ->  (deprecated)
```

The current state is the card's `status` field, not its directory location &mdash; cards live under `cards/` at every stage. Status transitions happen in PRs and are recorded by updating `status` and `modified_at`.

## How a card is checked

```
$ python scripts/verify.py            # verify every card
$ python scripts/verify.py cards/cc-3a7f2b91.json  # verify one
```

For `verbatim` cards the verifier confirms three things:
1. The card matches the schema.
2. The card's `source_hash` resolves to a real extracted source under `sources/extracted/` and that source's current hash still matches.
3. The `source_excerpt` appears as a contiguous substring of the extracted Markdown, and `back` is byte-identical to `source_excerpt`.

For `paraphrased` cards the verifier confirms (1) and (2), then defers to human PR review for (3) per AGENTS.md. The pipeline never auto-promotes paraphrased cards.

## Filename = id rule

The verifier enforces `card.id == filename stem`. This keeps the on-disk layout self-describing: you can identify a card from its path alone.
