"""Tests for webhook verification and prompt structure."""

from src.reviewer import build_review_prompt, verify_signature  # Import helper functions under test.


def test_verify_signature_accepts_valid_digest() -> None:
    """Signature helper should accept correctly signed payloads."""

    payload = b'{"action":"opened"}'  # Create deterministic payload bytes for signature test.
    secret = "my-secret"  # Define shared secret used by sender and receiver.
    import hashlib  # Import hashlib for digest generation in test.
    import hmac  # Import hmac to produce matching signature header.

    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()  # Compute expected signature digest.
    header = f"sha256={digest}"  # Format signature header as GitHub sends it.
    assert verify_signature(payload, header, secret) is True  # Ensure verification passes for correct signature.


def test_build_review_prompt_has_required_sections() -> None:
    """Prompt should include required structured review categories."""

    prompt = build_review_prompt("Add auth middleware", "Implements token checks.", "diff --git a/app.py b/app.py")  # Build sample review prompt.
    assert "1) Correctness" in prompt  # Ensure correctness section instruction is present.
    assert "4) Tests" in prompt  # Ensure tests section instruction is present.
    assert "Diff:" in prompt  # Ensure diff payload marker is included.
