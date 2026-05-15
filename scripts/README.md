# scripts/

Build and verification automation. No application code lives here.

## extract.py

Extracts source PDFs in [`sources/`](../sources/) to Markdown using [Marker](https://github.com/VikParuchuri/marker). Output goes to [`sources/extracted/`](../sources/extracted/) alongside a `sha256sum`-compatible hash file for each extraction.

**Prerequisites**
- NVIDIA GPU recommended (Marker is GPU-accelerated)
- Marker installed: `pipx install marker-pdf`

**Usage**
```
python scripts/extract.py                  # extract every PDF in sources/
python scripts/extract.py sources/foo.pdf  # extract a single PDF
python scripts/extract.py --force          # re-extract even if output exists
```

The hex digest in each `.sha256` file (with `sha256:` prefix) is what every card's `source_hash` field stores per [`cards/schema.json`](../cards/schema.json). When a source PDF is re-extracted and its hash changes, every card citing that source flips to "needs re-verification" automatically.

## verify.py

Verifies every card under [`cards/`](../cards/) against the extracted NIST source it cites. Stdlib only; no dependencies.

**Usage**
```
python scripts/verify.py                          # verify every card
python scripts/verify.py cards/cc-XXXXXXXX.json   # verify one
```

**What it checks**
- Schema: required fields present with correct types and values (manual checks against `cards/schema.json` &mdash; no `jsonschema` dependency)
- Provenance: `source_hash` resolves to an extracted source under `sources/extracted/` and that source's current hash still matches the value on the card
- `verbatim` cards: `source_excerpt` is a contiguous substring of the extracted source markdown, and `back` is byte-identical to `source_excerpt`
- `paraphrased` cards: defers to human PR review per [`AGENTS.md`](../AGENTS.md); reported as `[para]` so they aren't silently approved

Exit code is non-zero if any card fails a check the verifier owns.
