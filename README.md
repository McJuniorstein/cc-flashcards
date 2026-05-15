# CC Flashcards

> **Status: pre-launch.** Content pipeline in development. Public deployment will follow content verification.

A free, open-source study app for the ISC2&reg; Certified in Cybersecurity (CC) certification exam. Every flashcard is sourced verbatim from authoritative public-domain NIST publications and cites its source. No accounts, no tracking, no paywall.

## Why this exists

People preparing for the CC exam currently choose between paid practice tools, free decks of unverified quality, or the ISC2 official course (free for now, but ending May 2026). This project fills that gap with a free, source-verified deck &mdash; built to the security and privacy standards the subject matter teaches.

## How it works

- Definitions are pulled **verbatim** from NIST publications (public domain) and cited.
- A programmatic check verifies card text against the extracted source text.
- The small subset of cards that genuinely require paraphrase gets extra human review via GitHub PRs.
- All review history is public.

See [`AGENTS.md`](./AGENTS.md) for the verification contract.

## Status

Pre-content. Schema and verification pipeline are defined; cards have not yet been generated. Public Netlify deployment will happen only after the security checklist (see planning docs) passes.

## Project structure

| Path | Purpose |
|---|---|
| `AGENTS.md` | Verification protocol &mdash; the contract any contributor (human or agent) works against |
| `SECURITY.md` | Vulnerability disclosure policy |
| `cards/schema.json` | Card data schema |
| `sources/` | NIST source PDFs and extracted text |
| `docs/planning/` | Historical planning documents |
| `netlify.toml` | Security headers + build config |

## Licenses

- **Code:** MIT &mdash; see [`LICENSE`](./LICENSE)
- **Deck content:** CC0 1.0 Universal &mdash; see [`cards/LICENSE`](./cards/LICENSE)

## Disclaimer

*This is an independent, community-maintained study tool. It is not affiliated with, endorsed by, or sponsored by ISC2&reg;. ISC2&reg;, CISSP&reg;, CC&#8480;, and related marks are trademarks of ISC2, Inc.*

## Security

See [`SECURITY.md`](./SECURITY.md) for how to responsibly disclose vulnerabilities.
