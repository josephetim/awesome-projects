# A08 Software and Data Integrity Failures

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Software and data integrity failures happen when updates and artifacts are trusted without verification.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Inspect build/release pipelines for signature verification and tamper checks.

## How To Fix
Require signed artifacts and verify integrity before deployment and execution.
