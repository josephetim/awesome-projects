"""Secure controls for A08 Software and Data Integrity Failures."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A08 Software and Data Integrity Failures"],  # Identify protected category.
        "controls": [
            "Sign release artifacts and verify signatures before deployment.",  # Protect supply chain from tampered artifacts.
            "Pin trusted update sources and require checksum validation.",  # Prevent untrusted update injection.
            "Protect CI/CD credentials and enforce change approvals.",  # Reduce pipeline tampering risk.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
