# OWASP Top 10 Lab

This module maps each OWASP Top 10 category to:

1. plain-English explanation
2. DVWA/local-lab reproduction guidance
3. detection ideas
4. mitigation strategy
5. safe demo code

## Ethics Boundary

- Authorized-use only.
- Demo scripts are restricted to local lab targets.
- Never run these techniques against real systems.

## Included Categories

- A01 Broken Access Control
- A02 Cryptographic Failures
- A03 Injection
- A04 Insecure Design
- A05 Security Misconfiguration
- A06 Vulnerable and Outdated Components
- A07 Identification and Authentication Failures
- A08 Software and Data Integrity Failures
- A09 Security Logging and Monitoring Failures
- A10 Server-Side Request Forgery

## Run Tests

- `pytest tests/ -q`
