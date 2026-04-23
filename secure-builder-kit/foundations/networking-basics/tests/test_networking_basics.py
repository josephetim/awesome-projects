"""Tests for networking basics helpers."""

from src.networking_basics import explain_tcp_handshake  # Import function under test.


def test_explain_tcp_handshake_has_three_steps() -> None:
    """Handshake explanation should always include canonical 3 steps."""

    result = explain_tcp_handshake("localhost", 65535)  # Run handshake explanation against high local port.
    assert len(result["steps"]) == 3  # Ensure three-way handshake explanation has exactly three steps.
    assert isinstance(result["connection_successful"], bool)  # Ensure connection result is boolean for consistent downstream handling.
