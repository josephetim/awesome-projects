# SQL Injection Lab (DVWA Only)

## Ethics and Legal Boundary

This module is strictly for authorized local training.

- Allowed targets: local DVWA and intentionally vulnerable lab apps.
- Prohibited: real systems without explicit written authorization.

## What This Module Covers

- basic SQL injection
- UNION-based SQL injection
- blind boolean SQL injection
- blind time-based SQL injection

## Stack

- Python
- requests
- BeautifulSoup
- DVWA

## Walkthrough

1. Start DVWA locally at `http://localhost:8080`.
2. Log in and set DVWA security level to low (training mode).
3. Run one demo script:
   - `python basic_demo.py`
   - `python union_demo.py`
   - `python blind_boolean_demo.py`
   - `python blind_time_demo.py`
4. Observe behavior and compare with defensive examples.

## Defensive Focus

- Always use parameterized queries.
- Validate and constrain input types.
- Apply least privilege to DB users.

## Safe sqlmap Guidance (Documentation Only)

`sqlmap` can be useful in authorized labs, but this repository intentionally does not script `sqlmap` usage.

## Run Tests

- `pytest tests/ -q`
