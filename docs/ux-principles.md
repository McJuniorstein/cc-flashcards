# UX Principles

This document is the UX contract for CC Flashcards. It sits alongside [`AGENTS.md`](../AGENTS.md) (the data/verification contract). Both are enforced as acceptance criteria for the app, not aspirations.

**Principle version:** 1.0 (2026-05-15)

---

## The flashlight test

A cert study tool should behave like a good flashlight: **immediate, reliable, no fuss, works when needed, disappears into the background.** The target user is someone with 10 spare minutes at a coffee shop, an airport gate, or in their car. Any friction between "open" and "studying" loses them.

The metric that matters is **time-to-first-card.** Engagement, session length, return visits — none of those are goals. Helping someone learn the material is the only goal.

## Product rules (hard)

These are off-the-table for V1 and V2 alike:

- No onboarding flow, tutorial, carousel, or "welcome tour"
- No account, signup, or login wall &mdash; ever
- No streaks, badges, points, leaderboards, or gamification loops
- No motivational copy, mascot, or branded personality
- No "choose your learning journey" or pre-study quizzes
- No animated splash, intro video, or skippable cinematic
- No third-party JS on the critical path &mdash; analytics beacon is non-blocking and may degrade silently
- No tracking, fingerprinting, or behavioural analytics (per the privacy section of `docs/planning/`)

Progress is held in `localStorage` only. The site never asks the user for anything.

## Performance budgets (hard)

These are tested in CI before any release.

| Metric | V1 target | Hard ceiling |
|---|---|---|
| Largest Contentful Paint (LCP), broadband | < 1.0s | < 1.5s |
| LCP, simulated fast 3G | < 1.5s | < 2.5s |
| First Input Delay (FID) | < 50ms | < 100ms |
| Cumulative Layout Shift (CLS) | < 0.05 | < 0.1 |
| Total JS shipped (gzipped) | < 30KB | < 50KB |
| Total CSS shipped (gzipped) | < 10KB | < 20KB |
| HTML payload (initial) | < 15KB | < 30KB |
| Number of network requests, initial load | < 8 | < 12 |
| Lighthouse Performance | 100 target | >= 95 |
| Lighthouse Accessibility | 100 target | **100 required** |
| Lighthouse Best Practices | 100 target | 100 |
| Lighthouse SEO | >= 90 | n/a |

Notes:
- **Accessibility 100 is non-negotiable.** A study tool whose subject matter teaches "protect society" (ISC2 Canon 1) cannot itself exclude users on assistive tech. WCAG 2.1 AA is the floor.
- The 50KB JS ceiling exists to catch framework obesity in PR review. A static flashcard app over 50KB gzipped is a red flag, not a fact of life.
- Zero third-party blocking resources. Self-host fonts. Self-host the analytics script (Umami). Inline critical CSS only if it stays within the CSS budget.

## Architecture commitments

These directly affect the framework decision when Step 5 begins.

- **Offline-capable.** Service worker caches the deck and the app shell. Once a user has loaded the site, it works in airplane mode, behind captive portals, and on flaky mobile. The service worker is self-hosted under `'self'` &mdash; CSP-clean.
- **Static-first.** No runtime data fetching for cards. The verified deck is bundled at build time as a JSON file (or split per domain).
- **No client-side framework re-render on card flip.** Toggling a card's face is a CSS state change, not a React re-render cycle. Frameworks may be used for routing/state, but the per-card interaction is plain DOM.
- **Resumability.** The app remembers where the user left off across reloads, tabs, and offline sessions, entirely via `localStorage`. No server-side sync.
- **No build-time hostname coupling.** The same build runs at any URL &mdash; under a custom domain, on a Netlify preview, or served from `file://` for local review.

## Interaction model (locked)

Three interactions exist. Anything beyond these gets pushed back in PR review.

1. **Choose what to study** &mdash; all cards / by domain / random / cards marked review. One screen, no wizards.
2. **Flip the card** &mdash; one tap, one key, one swipe. Front shows term; back shows definition + source citation.
3. **Mark and advance** &mdash; "Known" or "Review again", then next card. Nothing else.

That's the whole app. Session timing, "study modes", "challenges", and similar are explicitly **not** features.

## Defer to design phase

The following are real questions that need answers, but **not now.** They are preserved here so they aren't forgotten when Step 5 (app build) begins.

- Visual design: typography choice, spacing system, colour palette, light/dark mode handling
- Keyboard shortcut mapping (spacebar to flip is the obvious default; what else?)
- Touch gestures: swipe direction conventions, threshold for "known" vs "review"
- Card flip animation: instant, fade, or 3D rotate? (Bias toward instant or a sub-100ms transition.)
- Domain selector UI: chips, dropdown, or filter buttons?
- Resume prompt vs silent resume on revisit
- How "review again" cards are surfaced &mdash; queue, weighted shuffle, or end-of-session block?
- Source citation presentation: inline on card back, hover/tap-to-reveal, or always visible?
- Empty-state and error-state copy
- 404 page

When Step 5 begins, this list gets a separate doc (`docs/design-decisions.md`) and each item is resolved with a written rationale.

## Updates to this document

Like `AGENTS.md`, this is a contract. Changes require a CHANGELOG entry and a protocol version bump. The default answer to "should we add X feature?" is **no**, and the burden of proof sits with the proposer.
