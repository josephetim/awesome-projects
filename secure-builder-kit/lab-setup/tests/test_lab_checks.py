"""Tests for lab endpoint checks."""

from src.lab_checks import is_port_open  # Import function under test.


def test_is_port_open_returns_boolean() -> None:
    """Port check helper should always return a boolean."""

    result = is_port_open("127.0.0.1", 65534)  # Check an arbitrary high local port to validate function behavior.
    assert isinstance(result, bool)  # Ensure helper returns bool type for caller predictability.
