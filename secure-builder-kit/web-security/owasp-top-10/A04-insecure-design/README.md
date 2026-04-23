# A04 Insecure Design

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Insecure design means core workflows lack security controls because threat modeling and abuse-case planning were skipped.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Review architecture decisions, trust boundaries, and missing abuse-case controls before implementation.

## How To Fix
Integrate threat modeling and secure design patterns at planning time, not after deployment.
