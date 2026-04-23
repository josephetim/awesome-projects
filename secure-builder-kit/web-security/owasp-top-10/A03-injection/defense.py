"""Secure controls for A03 Injection."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A03 Injection"],  # Identify protected category.
        "controls": [
            "Use parameterized database queries for all user-driven input.",  # Prevent SQL command injection through query concatenation.
            "Validate and sanitize input based on strict allowlists.",  # Reduce malformed or malicious interpreter input.
            "Apply least-privilege DB accounts and query limits.",  # Limit blast radius when injection attempts occur.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
