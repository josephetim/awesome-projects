"""Secure controls for A10 Server-Side Request Forgery."""

from __future__ import annotations


def secure_controls() -> dict[str, list[str]]:
    """Return practical mitigation controls."""

    return {
        "category": ["A10 Server-Side Request Forgery"],  # Identify protected category.
        "controls": [
            "Allowlist approved outbound domains for server fetch features.",  # Restrict destination scope to trusted targets.
            "Block internal/private IP ranges and metadata endpoints.",  # Prevent access to internal infrastructure via SSRF.
            "Validate and normalize URLs before requests are executed.",  # Reduce parser confusion and bypass tricks.
        ],
    }


if __name__ == "__main__":
    print(secure_controls())  # Print controls for quick reference.
