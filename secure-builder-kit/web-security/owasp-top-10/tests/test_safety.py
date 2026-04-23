"""Tests for OWASP safety helpers."""

import pytest  # Import pytest for exception assertions.

from src.safety import require_local_target  # Import local-target guard under test.


def test_require_local_target_accepts_localhost() -> None:
    """Safety check should allow localhost target."""

    require_local_target("http://localhost:8080")  # Validate localhost target passes safety check.


def test_require_local_target_rejects_remote_host() -> None:
    """Safety check should block non-local targets."""

    with pytest.raises(ValueError):  # Expect ValueError for non-local target.
        require_local_target("http://example.com")  # Validate remote host target is rejected.
