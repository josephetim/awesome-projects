"""Secure controls for A02 Cryptographic Failures."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A02 Cryptographic Failures"],  # Identify protected category.
        "controls": [
            "Use modern encryption and enforce TLS for sensitive data paths.",  # Protect confidentiality in transit and at rest.
            "Store and rotate keys securely using dedicated secret management.",  # Prevent key disclosure and long-lived compromise.
            "Avoid custom crypto and weak/deprecated algorithms.",  # Reduce implementation and algorithmic risk.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
