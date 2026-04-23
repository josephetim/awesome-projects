"""Secure controls for A01 Broken Access Control."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A01 Broken Access Control"],  # Identify protected category.
        "controls": [
            "Enforce authorization checks on every protected endpoint.",  # Apply server-side access control consistently.
            "Use object-level ownership validation for direct object references.",  # Prevent horizontal privilege escalation.
            "Deny by default and allow by explicit policy.",  # Reduce accidental over-permission.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
