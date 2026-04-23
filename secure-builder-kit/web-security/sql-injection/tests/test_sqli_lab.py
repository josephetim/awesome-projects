"""Tests for SQL injection lab safety and payload utilities."""

import pytest  # Import pytest for exception assertion support.

from src.sqli_lab import basic_payloads, require_local_dvwa_target  # Import functions under test.


def test_require_local_dvwa_target_rejects_remote() -> None:
    """Safety checker should reject non-local targets."""

    with pytest.raises(ValueError):  # Expect ValueError for unsafe target host.
        require_local_dvwa_target("http://example.com")  # Validate remote host is blocked.


def test_basic_payloads_non_empty() -> None:
    """Basic payload helper should provide at least one payload."""

    assert len(basic_payloads()) >= 1  # Ensure payload list is non-empty for demo usability.
