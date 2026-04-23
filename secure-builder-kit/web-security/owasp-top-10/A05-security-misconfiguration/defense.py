"""Secure controls for A05 Security Misconfiguration."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A05 Security Misconfiguration"],  # Identify protected category.
        "controls": [
            "Disable debug endpoints and remove default credentials.",  # Eliminate common misconfiguration exposure points.
            "Apply secure HTTP headers and strict service permissions.",  # Reduce accidental metadata and attack surface leakage.
            "Use infrastructure-as-code baselines with continuous drift checks.",  # Keep configurations secure over time.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
