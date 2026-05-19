# CC Flashcards

> ## :construction: Work in progress &mdash; not ready for use
>
> This project is in active development. The deck is incomplete, no public site is deployed, and the verification pipeline is still being exercised. **Do not use this as a sole study resource for the CC exam yet.** Watch the repo for updates; an announcement will go on the README when V1 is actually shipped.

A free, open-source study app for the ISC2&reg; Certified in Cybersecurity (CC) certification exam. Every flashcard is sourced verbatim from authoritative public-domain NIST publications and cites its source. No accounts, no tracking, no paywall.

## Why this exists

People preparing for the CC exam currently choose between paid practice tools, free decks of unverified quality, or the ISC2 official course (free for now, but ending May 2026). This project fills that gap with a free, source-verified deck &mdash; built to the security and privacy standards the subject matter teaches.

## How it works

- Definitions are pulled **verbatim** from NIST publications (public domain) and cited.
- A programmatic check verifies card text against the extracted source text.
- The small subset of cards that genuinely require paraphrase gets extra human review via GitHub PRs.
- All review history is public.

See [`AGENTS.md`](./AGENTS.md) for the verification contract.

## Status (as of 2026-05-18)

| Area | State |
|---|---|
| Verification protocol (`AGENTS.md`) | Locked at v1.1 |
| UX principles (`docs/ux-principles.md`) | Locked at v1.0 |
| Source corpus | 9 NIST PDFs + CNSSI 4009 + IETF RFC 4949, all extracted to Markdown |
| Card schema | Defined and in use |
| Extraction pipeline (`scripts/extract.py`) | Working |
| Verifier (`scripts/verify.py`) | Working, with normalization layer for Marker artifacts; validates `source_chain` shape |
| **Deck** | **107 cards: 91 verified, 16 draft (pending PR review). Covers all 5 CC domains; D4 went from 1 → 33 across three CNSSI 4009 / 800-41 / 800-94 / RFC 4949 sessions.** |
| **App** | **Not started.** No framework chosen, no build, no deployment. |
| **Netlify deployment** | **Not deployed.** Pending content completion and the security checklist. |

### Domain distribution vs exam weighting

| Domain | Cards | Deck % | Exam % | Status |
|---|---|---|---|---|
| D1 Security Principles | 25 | 23% | 26% | aligned |
| D2 BC/DR/IR | 13 | 12% | 10% | aligned |
| D3 Access Controls | 19 | 18% | 22% | slightly under |
| D4 Network Security | 33 | 31% | 24% | over (was severely under; now well-supported) |
| D5 Security Operations | 17 | 16% | 18% | aligned |

The deck has reached the "worthwhile study pack" range (107 cards, target was 110&ndash;130). D4 is now over-represented vs its exam weight, but that's an over-correction from being at 1% &mdash; D4 content depth is now strong. Future content batches should skew D1, D3, or D5 (or add a few primitive D4 cards once more sources are added). Known content gaps and provenance flags are tracked in `CHANGELOG.md`.

## Project structure

| Path | Purpose |
|---|---|
| `AGENTS.md` | Verification protocol &mdash; the contract any contributor (human or agent) works against |
| `docs/ux-principles.md` | UX contract &mdash; product rules, performance budgets, architecture commitments |
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
