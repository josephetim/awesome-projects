"""Shared local-target safety checks for OWASP demo scripts."""

from __future__ import annotations

from urllib.parse import urlparse  # Import urlparse for host validation in URL safety checks.


def is_local_lab_target(url: str) -> bool:
    """Return True only for localhost/loopback targets."""

    parsed = urlparse(url)  # Parse URL into components for host validation.
    host = (parsed.hostname or "").strip().lower()  # Extract normalized hostname string.
    return host in {"localhost", "127.0.0.1"}  # Allow only loopback hosts for safe demo execution.


def require_local_target(url: str) -> None:
    """Raise error when target URL is not local-lab safe."""

    if not is_local_lab_target(url):  # Enforce strict local-target boundary.
        raise ValueError("Safety check failed: target must be localhost or 127.0.0.1.")  # Raise explicit safety error.
