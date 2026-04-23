# A07 Identification and Authentication Failures

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Identification and authentication failures occur when account verification and session controls are weak.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Test MFA, password policy, lockout, and session token handling flows.

## How To Fix
Use strong authentication controls, secure session management, and abuse-rate protections.
