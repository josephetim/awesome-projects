"""Secure controls for A09 Security Logging and Monitoring Failures."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A09 Security Logging and Monitoring Failures"],  # Identify protected category.
        "controls": [
            "Log authentication, authorization, and privilege-change events.",  # Capture high-value security telemetry.
            "Configure alerting for anomalous activity and repeated failures.",  # Detect incidents earlier.
            "Define and rehearse incident response playbooks.",  # Improve operational response effectiveness.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
