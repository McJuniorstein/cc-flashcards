# Security Policy

This project hosts a study tool for security practitioners. Its own security posture is treated as a primary quality signal.

## Reporting a vulnerability

**Preferred channel:** open a private security advisory via GitHub:
[https://github.com/McJuniorstein/cc-flashcards/security/advisories/new](https://github.com/McJuniorstein/cc-flashcards/security/advisories/new)

Please do **not** file public issues for vulnerability reports.

## What's in scope

- The deployed Netlify site (once live)
- The build configuration (`netlify.toml`)
- Application source code under `/app` (once live)
- Pipeline scripts under `/scripts` (once live)

## What's out of scope

- Vulnerabilities in Netlify itself &mdash; report to Netlify
- Vulnerabilities in upstream dependencies &mdash; please also report upstream
- Issues in NIST source documents &mdash; report to NIST
- Social engineering, physical attacks, or denial-of-service testing against the deployed site

## Response timeline

- **Acknowledgement:** within 7 days of report
- **Triage + fix or explanation:** within 30 days
- **Public disclosure:** coordinated with the reporter

## Recognition

Reporters who follow responsible disclosure are credited in `CHANGELOG.md` unless they prefer to remain anonymous.
