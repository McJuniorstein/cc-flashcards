# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository skeleton
- Card schema (`cards/schema.json`) with `verbatim` and `paraphrased` answer types
- Verification protocol (`AGENTS.md`) &mdash; NIST verbatim text is the source of truth
- UX principles (`docs/ux-principles.md`) &mdash; product rules, performance budgets, and architecture commitments locked in before any UI work begins
- Vulnerability disclosure policy (`SECURITY.md`)
- Strict security-header configuration (`netlify.toml`)
- Pre-commit hooks: `gitleaks` for secret scanning, basic hygiene checks
- MIT license for code, CC0 1.0 Universal for deck content
- Planning docs preserved under `docs/planning/`
- NIST SP 1308 (CSF 2.0 Quick-Start Guide) as first source PDF
