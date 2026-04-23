# A10 Server-Side Request Forgery

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
SSRF happens when server-side fetch features can be abused to access internal or restricted network resources.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Test URL-fetching endpoints for access to internal addresses and metadata services.

## How To Fix
Allowlist outbound destinations and block internal address ranges by policy.
