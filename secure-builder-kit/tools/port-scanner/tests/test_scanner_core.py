"""Tests for port scanner core helpers."""

from src.scanner_core import expand_targets, parse_ports  # Import helpers under test.


def test_expand_targets_single_host() -> None:
    """Single host should remain single-item list."""

    assert expand_targets("127.0.0.1") == ["127.0.0.1"]  # Verify single-host expansion behavior.


def test_parse_ports_mixed_spec() -> None:
    """Mixed range/list spec should produce sorted unique ports."""

    assert parse_ports("80,22,1000-1002") == [22, 80, 1000, 1001, 1002]  # Verify deterministic parsing and ordering.
