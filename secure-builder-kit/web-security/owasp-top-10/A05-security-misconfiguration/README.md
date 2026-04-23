# A05 Security Misconfiguration

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Security misconfiguration exposes systems via unsafe defaults, unnecessary services, or weak deployment settings.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Scan for debug mode, default credentials, insecure headers, and open admin surfaces.

## How To Fix
Harden configuration baselines and automate secure environment checks.
