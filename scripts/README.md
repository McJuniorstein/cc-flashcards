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
