"""Secure controls for A06 Vulnerable and Outdated Components."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A06 Vulnerable and Outdated Components"],  # Identify protected category.
        "controls": [
            "Maintain a software bill of materials for dependency visibility.",  # Track components and versions centrally.
            "Scan dependencies continuously for known vulnerabilities.",  # Detect outdated/high-risk packages quickly.
            "Patch critical CVEs with defined SLA and rollback testing.",  # Reduce exploit window while preserving reliability.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
