"""Run basic SQL injection payloads against local DVWA only."""

from __future__ import annotations

import os  # Import os to read local DVWA base URL from environment.

from src.sqli_lab import basic_payloads, run_demo  # Import basic payloads and generic demo runner.

if __name__ == "__main__":
    base_url = os.getenv("DVWA_BASE_URL", "http://localhost:8080")  # Read local DVWA URL with safe default.
    print(run_demo(base_url, basic_payloads()))  # Execute and print basic SQLi demo results.
