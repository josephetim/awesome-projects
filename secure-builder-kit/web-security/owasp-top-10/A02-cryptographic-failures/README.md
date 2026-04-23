# A02 Cryptographic Failures

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Cryptographic failures expose sensitive information because encryption, key handling, or transport security is weak.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Inspect data-at-rest and data-in-transit protections, weak cipher usage, and key storage practices.

## How To Fix
Use modern encryption, secure key management, and enforce TLS for all sensitive communication.
