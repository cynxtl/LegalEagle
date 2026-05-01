# Security Policy

LegalEagle is currently an MVP intended for local development and evaluation.

## Supported Versions

Security fixes should target the current `main` branch unless release branches are introduced later.

## Reporting a Vulnerability

If you find a security issue, please do not open a public issue with exploit details. Contact the maintainers privately, or open a minimal public issue asking for a security contact if no private channel is available yet.

Include:

- Affected component
- Reproduction steps
- Impact
- Suggested fix, if known

## Current Security Status

- Authentication is not enabled for the MVP.
- CORS may allow all origins for local development.
- Uploaded documents may contain sensitive legal information and should not be committed.
- Model weights and private indexes should not be committed.

See [docs/SECURITY.md](docs/SECURITY.md) for implementation notes before production deployment.

