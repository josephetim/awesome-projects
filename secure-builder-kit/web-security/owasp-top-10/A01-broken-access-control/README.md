# A01 Broken Access Control

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Broken access control allows users to perform actions they should not be allowed to perform.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Test role boundaries and object ownership checks on server-side endpoints.

## How To Fix
Enforce deny-by-default authorization checks for every sensitive resource.
