"""Run blind time-based SQL injection payload against local DVWA only."""

from __future__ import annotations

import os  # Import os to read local DVWA base URL from environment.

from src.sqli_lab import blind_time_payloads, run_time_demo  # Import blind time payload and timed demo runner.

if __name__ == "__main__":
    base_url = os.getenv("DVWA_BASE_URL", "http://localhost:8080")  # Read local DVWA URL with safe default.
    payload = blind_time_payloads()[0]  # Select first time-based payload for demo execution.
    print(run_time_demo(base_url, payload))  # Execute and print timed SQLi demo result.
