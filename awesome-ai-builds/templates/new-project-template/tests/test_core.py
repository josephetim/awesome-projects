"""Tests for template core logic."""

import pytest  # Import pytest for assertion helpers and exception checks.

from src.core import transform_text  # Import function under test from source package.


def test_transform_text_uppercases_and_trims() -> None:
    """Template function should normalize and uppercase text."""

    assert transform_text("  hello  ") == "HELLO"  # Verify trimming and uppercase conversion in one assertion.


def test_transform_text_rejects_empty() -> None:
    """Template function should reject blank input."""

    with pytest.raises(ValueError):  # Assert that blank input triggers explicit validation behavior.
        transform_text("   ")  # Pass whitespace-only input to exercise empty-input branch.
