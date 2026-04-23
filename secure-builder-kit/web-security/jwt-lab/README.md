# JWT Lab

## Ethics and Legal Boundary

This lab is for authorized local education only.

- Run only against included vulnerable demo app.
- Never test real production APIs without explicit written permission.

## What This Module Demonstrates

- `alg:none` attack
- weak HMAC secret brute force
- RS256 to HS256 confusion attack

## Structure

- `vulnerable-app/`: intentionally broken JWT validation flows
- `secure-app/`: corrected implementations
- `attacks/`: educational exploit scripts for local demo apps

## Run Locally

1. `cd web-security/jwt-lab`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. Start vulnerable app: `uvicorn main:app --app-dir vulnerable-app --reload --port 8001`
6. Start secure app: `uvicorn main:app --app-dir secure-app --reload --port 8002`
7. Run attack demos from `attacks/` against vulnerable app only

## Docker

- `docker compose up --build`

Services:
- Vulnerable app: `http://localhost:8001`
- Secure app: `http://localhost:8002`

## Run Tests

- `pytest tests/ -q`
