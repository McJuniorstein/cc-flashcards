# CC Flashcards — Planning Doc

**Project:** Free, open-source study app for the ISC2® Certified in Cybersecurity (CC) certification exam
**Date:** 14 May 2026
**Status:** Planning — v3

> Independent project. Not affiliated with, endorsed by, or sponsored by ISC2.

---

## 1. What This Is

A free web app that lets people studying for the **ISC2 Certified in Cybersecurity (CC) exam** practice with flashcards drawn from authoritative source material. Every card is verified against its source by multi-model fact-checking before it ships. Every card cites its source. Users get content they can trust without paying for it — and the site itself is built to the same security and privacy standards the subject matter teaches.

## 2. Why This Should Exist

People preparing for the CC exam currently choose between:
- Paid practice tools ($30–$200+) of varying quality
- Free flashcard decks on Quizlet/Anki of unverified, often-wrong content
- The ISC2 official course (free for now, but ending May 2026)

There is no free, public, source-verified study deck for the CC. This project fills that gap — and demonstrates that a study tool for security professionals can be built to security-professional standards.

## 3. Success Criteria

The project succeeds when **all** of these are true:

- [ ] ~150–200 flashcards covering all five CC exam domains, each verified against authoritative sources
- [ ] Every card has a source citation users can click through to verify
- [ ] App is publicly deployed, works on desktop and mobile, requires no signup
- [ ] Site ships with proper security headers, no known vulnerabilities, no tracking cookies
- [ ] Privacy policy is honest about what's collected and what isn't
- [ ] At least one independent user (not the creator) reports using it productively
- [ ] Verification pipeline is reproducible — anyone forking the repo can regenerate or expand the deck

Failure modes to avoid:
- Becoming "yet another flashcard deck of dubious quality"
- Shipping a security study site with security problems
- Tracking users in ways the subject matter would condemn

## 4. Scope — V1

### In scope

- **Content:** ISC2 CC exam outline as the spine; definitions sourced from NIST publications (NIST SP 800-12 Rev 1, NIST CSF 2.0, NIST SP 800-27 Rev A definitions where cited by ISC2, NIST SP 800-53, NIST SP 800-61, NIST SP 800-34)
- **Five domains:** Security Principles, BC/DR/IR Concepts, Access Controls, Network Security, Security Operations
- **App:** Static web app, card flip, mark known/unknown, filter by domain, basic progress display
- **Persistence:** localStorage only — user progress stays in their browser
- **Hosting:** Free public hosting (Netlify free tier)
- **Mobile:** Responsive, usable on phone
- **Analytics:** Privacy-respecting, aggregate-only

### Explicitly out of scope (V1)

- User accounts / auth / sync across devices
- Backend / database / server-side state
- Multiple cert tracks (Security+, SSCP, CISSP, etc.) — possible V2
- Spaced repetition algorithm (Anki-style scheduling) — possible V2
- Quizzes, mock exams, timed practice modes — possible V2
- Native mobile app
- Community features (user-submitted cards, comments, leaderboards)
- AI tutor / chat against the content
- Per-user analytics / behavioral tracking
- Third-party advertising (forever, not just V1)

**Scope rule:** anything on the "out of scope" list stays out until V1 has shipped publicly and seen at least one month of real use.

## 5. Source Strategy

### Why NIST as the primary content source
- NIST publications are **US government works in the public domain** — no copyright, no licensing, free to reproduce and build upon
- ISC2's CC course material itself cites NIST sources for foundational definitions
- Using the same source ISC2 uses ensures alignment with exam content

### Primary sources
- **ISC2 CC Exam Outline** — defines what's *on* the exam (used for structure and topic coverage, not verbatim text)
- **NIST SP 800-12 Rev 1** — An Introduction to Information Security
- **NIST CSF 2.0** — Cybersecurity Framework
- **NIST SP 800-27 Rev A** — historical foundational definitions still cited by ISC2
- **NIST SP 800-53 Rev 5** — Security and Privacy Controls
- **NIST SP 800-61 Rev 2** — Computer Security Incident Handling Guide
- **NIST SP 800-34** — Contingency Planning Guide

### Storage
- All source PDFs stored in `/sources/` and versioned in git
- `/sources/README.md` lists each document with its NIST URL and download date
- Cards reference the document name and (where applicable) section

### Citation rule
- Every card has a `source` field naming the document
- If a definition originated in a withdrawn NIST publication that ISC2 still cites, cite it the way ISC2 does
- Citations are surfaced in the UI so users can verify any card against its source

## 6. Content Pipeline

Four phases, designed to produce verified content before any app code is written.

### Phase A — Research
- Agent reads ISC2 CC exam outline
- Identifies candidate terms and concepts per domain
- Cross-references with stored NIST sources
- Produces first-draft card set as JSON
- Output: `/cards/draft/` with raw candidate cards

### Phase B — Verification
- Each card passed through multiple models (Claude, GPT, Gemini)
- Each model verifies the card against its cited source PDF
- Each model returns: pass / fail / flag with reasoning
- Disagreements generate an HTML report (see Section 7)

### Phase C — Human review
- Human opens the HTML verification report
- Reviews flagged or disagreeing cards
- Approves, edits, or rejects each
- Approved cards move to `/cards/verified/`

### Phase D — App build
- App pulls verified cards
- Build, test, deploy
- No app work begins until verified content exists

## 7. Verification Protocol (the AGENTS.md contract)

`AGENTS.md` at repo root defines the verification protocol. Markdown by design — it's the contract agents read, not output for humans.

### Per-card verification checklist

Each card must pass all five:
1. Does the back-of-card text match the cited source text within acceptable paraphrase tolerance?
2. Is the source citation accurate (correct document, correct section if specified)?
3. Is the domain assignment correct (1 through 5)?
4. Does the card contradict any other card already in the deck?
5. Is the front-of-card question unambiguous given the back-of-card answer?

### Disagreement resolution rule

- **Unanimous pass** → card approved, moves to verified set
- **Any model flags or fails** → card moves to disagreements queue, human review required
- Humans break ties; no model tiebreaker

### Verification output format

- Each verification run produces one HTML report in `/reports/`
- Filename: `YYYY-MM-DD_HHMM__verification__pass-N.html`
- Report displays each card front/back, the source text excerpt, each model's verdict color-coded by agreement, with approve/reject UI

## 8. IP, Trademarks, and Disclaimers

### What's allowed
- Referencing the cert by name ("ISC2 Certified in Cybersecurity" or "ISC2 CC")
- Citing ISC2 publications when sourcing definitions
- Reproducing NIST publication content (public domain)
- Using domain structure and topic coverage from the ISC2 exam outline

### What's prohibited
- Using the ISC2 logo, branded color scheme, or visual identity
- Implying endorsement, affiliation, partnership, or "official" status
- Reproducing actual ISC2 exam questions
- Copying the ISC2 CBK or course material verbatim — paraphrase and cite

### Required disclaimer

Must appear in app footer, README, and repo description:

> *This is an independent, community-maintained study tool. It is not affiliated with, endorsed by, or sponsored by ISC2®. ISC2®, CISSP®, CC℠, and related marks are trademarks of ISC2, Inc.*

### Trademark notation

First reference in any document or page: **ISC2®**
Subsequent references: ISC2 (unmarked is fine after first use)

## 9. Privacy & Analytics

The project follows the principle: **measure the site, not the user.**

### What gets collected (aggregate, anonymous)
- Page views (which domains/cards are most visited)
- Session duration (how long people study)
- Country-level location (no IP storage)
- Referrer source (how people find the site)
- Device class (desktop vs mobile, for design priorities)
- Browser class (for compatibility decisions)

### What does NOT get collected
- IP addresses (beyond brief processing for country-level lookup, then discarded)
- Personal identifiers
- Cross-site behavior
- Cookies of any kind, including session cookies
- localStorage data (study progress stays on user's device, never sent to any server)
- Anything that would require a GDPR consent banner

### Analytics tooling — preferred options

- **Plausible** — paid SaaS (~$9/mo for small site), EU-hosted, no cookies, GDPR-compliant by design
- **Umami** — open source, self-hostable for free on a small VPS, similar feature set to Plausible
- **GoatCounter** — free tier for small sites, lightweight, privacy-first

**Explicitly rejected:** Google Analytics, Facebook Pixel, Hotjar, FullStory, anything that builds user profiles, anything requiring a consent banner.

### Third-party data processing — transparency requirement

The site is hosted on Netlify, which processes incoming requests and maintains server-side logs per their privacy policy. The privacy policy on the site must disclose:

- That Netlify is the hosting provider
- That Netlify's privacy policy governs the data they process at the network/CDN layer
- That this data is outside the project's direct control
- A link to Netlify's privacy policy

Same disclosure pattern applies to whichever analytics tool is chosen.

### Privacy policy

A dedicated `/privacy` page on the site. Plain language, no legalese, accurate. Must list:
- What's collected and why
- What's not collected
- Third parties involved (host, analytics provider)
- How localStorage works (and that it never leaves the device)
- Contact for privacy questions

## 10. Security Posture

**Principle:** the site practices the principles its content teaches. A study tool for security professionals must itself be a credible piece of security work.

This is not overkill — it is the project's most important quality signal.

### Required security measures

**Transport & headers**
- HTTPS only, redirect HTTP → HTTPS
- HSTS header with `max-age=31536000; includeSubDomains; preload`
- Content Security Policy (CSP) header restricting what the page can load
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (or equivalent via CSP `frame-ancestors`)
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy` restricting unused browser features

Netlify configures most of these via `_headers` file or `netlify.toml`.

**Code & dependencies**
- All dependencies pinned to specific versions
- Dependabot or Renovate enabled for automated security updates
- No unused dependencies
- Subresource Integrity (SRI) hashes on any CDN-loaded scripts (preferred: self-host everything, eliminate the question entirely)
- No mixed content (HTTP resources on HTTPS page)
- No inline scripts or styles (CSP-clean by design)

**Input handling**
- V1 has no user input, but localStorage reads must be treated as untrusted (someone could manually edit localStorage and inject content)
- All localStorage values validated before rendering
- HTML rendering uses safe DOM methods (`textContent` not `innerHTML`) by default

**Transparency & disclosure**
- Public repo on GitHub — open source allows audit by anyone
- `SECURITY.md` file in the repo describing how to report vulnerabilities
- `/.well-known/security.txt` file on the site with the same info
- Disclosure policy: acknowledge reports within 7 days, fix or explain within 30

**Compliance with ISC2 Code of Ethics**

The Code's four canons apply to this project as much as to professional work:

- **Canon 1 (protect society):** ship a site that won't harm users — no malware injection vectors, no leaked PII, no insecure dependencies serving CC candidates
- **Canon 2 (act honorably):** transparent privacy policy, accurate disclaimers, honest about limitations of the deck
- **Canon 3 (serve principals):** users of the site are the principals — their interests govern decisions about features, privacy, monetization (which is: none)
- **Canon 4 (advance and protect the profession):** ship something that reflects well on cybersecurity practitioners, not poorly

### Pre-launch security checklist

Before the public Netlify URL is shared anywhere:

- [ ] All security headers verified via securityheaders.com (target: A+)
- [ ] Mozilla Observatory scan passes (target: A or better)
- [ ] No high or critical vulnerabilities in `npm audit` / equivalent
- [ ] `SECURITY.md` and `security.txt` published
- [ ] Privacy policy live at `/privacy`
- [ ] Disclaimer live in footer
- [ ] HTTPS enforced, HSTS in place
- [ ] CSP set and tested in report-only mode first, then enforced

## 11. Repo Structure

```
cc-flashcards/
├── AGENTS.md                  # Verification protocol & instructions
├── README.md                  # Project overview, usage, attribution
├── SECURITY.md                # Vulnerability disclosure policy
├── LICENSE                    # MIT (likely)
├── CHANGELOG.md
├── /sources/                  # NIST + ISC2 source PDFs
│   ├── README.md
│   └── *.pdf
├── /cards/
│   ├── draft/                 # Raw agent output, pre-verification
│   ├── verified/              # Approved cards only
│   └── schema.json
├── /reports/                  # HTML verification reports
│   └── *.html
├── /app/                      # The web app
│   ├── public/
│   │   └── .well-known/
│   │       └── security.txt
│   ├── src/
│   └── package.json
├── /scripts/                  # Verification orchestration
└── netlify.toml               # Headers, redirects, build config
```

## 12. Tech Stack — Decisions Deferred

| Decision | Options | Defer until |
|---|---|---|
| Framework | React / Vanilla JS / SvelteKit | After content is locked |
| Styling | Tailwind + shadcn/ui / Tailwind alone / vanilla CSS | After framework chosen |
| Card data format | JSON / Markdown frontmatter | During Phase A |
| Build tool | Vite / no build | After framework chosen |
| Analytics provider | Plausible / Umami / GoatCounter | Before public launch |
| License | MIT / Apache 2.0 | Before public push |

## 13. Phasing

| Phase | Focus | Output |
|---|---|---|
| 1 — Setup | Repo, sources downloaded, AGENTS.md, license, SECURITY.md | Repo skeleton |
| 2 — Research | Agent generates draft cards across all domains | ~150–200 draft cards |
| 3 — Verification | Multi-model verification runs, produces HTML reports | First verification report |
| 4 — Review | Human review of disagreements, content locked | Verified card set |
| 5 — Build | App built, security headers configured, privacy policy written | Pre-launch state |
| 6 — Security pass | Headers scan, dep audit, observatory scan, fix findings | A+ security grade |
| 7 — Launch | Deploy to Netlify, share publicly | Public URL |
| 8 — Iterate | Real user feedback, card corrections | Improved deck over time |

Quality of content and security posture gate progression, not calendar dates.

## 14. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| AI hallucinates definitions | Multi-model verification, mandatory source citation, human review on disagreements |
| Scope creep | Out-of-scope list in Section 4. Re-read before adding anything. |
| Polish over substance | Content quality and security posture are V1 success metrics |
| Build before content ready | Phase 5 cannot start until verified content exists |
| Trademark/IP concerns | Section 8 governs every public-facing surface |
| Security vulnerabilities ship to users | Section 10 checklist must pass before public launch |
| Privacy promises drift over time | Privacy policy is reviewed every time analytics or hosting changes |
| Source documents change (NIST updates) | PDFs versioned in repo; cards can be re-verified against locked source state |
| Project becomes abandoned | Open source license allows others to fork and continue |

## 15. Open Questions

- [ ] Plausible (paid, simple) or self-hosted Umami (free, more infrastructure)?
- [ ] How are verification disagreements edited — HTML report UI or JSON file directly?
- [ ] Where do user-reported card errors get collected post-launch — GitHub issues, in-app form, both?
- [ ] License: MIT (maximum freedom) or Apache 2.0 (patent grant)?
- [ ] What happens to cards that fail verification and don't get rescued in review?

## 16. Definition of Done

V1 is done when:

- The app loads at a public URL with valid HTTPS
- All five CC domains have verified flashcards
- Security headers earn an A+ on securityheaders.com
- Mozilla Observatory scan passes at A or better
- `SECURITY.md` and `security.txt` are published
- Privacy policy is live and accurate
- Required disclaimer appears in app footer and README
- Repo is public with a clear license
- At least one external user has used it and reported back

Beyond that is V2.

---

**Last updated:** 14 May 2026
**Next review:** when Phase 2 draft cards exist
