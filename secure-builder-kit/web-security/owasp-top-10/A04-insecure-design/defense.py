"""Secure controls for A04 Insecure Design."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A04 Insecure Design"],  # Identify protected category.
        "controls": [
            "Perform threat modeling before implementation begins.",  # Identify abuse paths early in architecture decisions.
            "Define security requirements as first-class acceptance criteria.",  # Ensure controls are built into design from the start.
            "Review trust boundaries and failure modes for every critical workflow.",  # Reduce systemic design-level weaknesses.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
