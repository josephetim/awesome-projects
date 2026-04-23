# A09 Security Logging and Monitoring Failures

## Ethics Boundary
Use this only in local authorized labs.

## Plain-English Explanation
Logging and monitoring failures prevent timely detection and response to attacks and abuse.

## DVWA Reproduction Steps
1. Run DVWA locally.
2. Authenticate to DVWA.
3. Run `exploit.py` against `http://localhost:8080`.

## How To Detect
Review log coverage and alerting around authentication, authorization, and sensitive operations.

## How To Fix
Implement structured logging, actionable alerts, and practiced incident-response workflows.
