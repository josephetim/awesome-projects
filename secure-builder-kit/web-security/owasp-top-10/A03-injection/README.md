# A03 Injection

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Injection occurs when untrusted input is interpreted as commands or queries by backend components.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Review dynamic query construction and run controlled payload tests against input fields.

## How To Fix
Use parameterized queries, strict allowlist validation, and output encoding where relevant.
