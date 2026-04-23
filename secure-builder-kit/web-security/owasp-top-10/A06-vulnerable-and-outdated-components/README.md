# A06 Vulnerable and Outdated Components

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Vulnerable and outdated components expose known weaknesses that attackers can exploit without novel techniques.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Inventory dependencies and compare versions against known CVE advisories.

## How To Fix
Patch components promptly and enforce update governance in CI/CD.
