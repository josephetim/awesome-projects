"""Tests for packet summary extraction."""

from src.analyzer import summarize_packet  # Import packet summary helper under test.


class FakeLayer:
    """Simple fake protocol layer object for tests."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # Populate layer attributes from keyword arguments.


class FakePacket:
    """Simple fake packet with scapy-like API."""

    def __init__(self, layers):
        self.layers = layers  # Store layer map by layer name.

    def haslayer(self, name: str) -> bool:
        return name in self.layers  # Return layer presence boolean.

    def getlayer(self, name: str):
        return self.layers[name]  # Return fake layer object by name.


def test_summarize_packet_tcp() -> None:
    """Summary helper should extract TCP metadata from packet."""

    packet = FakePacket(  # Build fake packet containing IP and TCP layers.
        {
            "IP": FakeLayer(src="10.0.0.1", dst="10.0.0.2"),  # Provide IP layer fields.
            "TCP": FakeLayer(sport=1234, dport=80),  # Provide TCP layer fields.
        }
    )
    summary = summarize_packet(packet)  # Summarize fake packet.
    assert summary["protocol"] == "TCP"  # Verify protocol classification.
    assert summary["src"] == "10.0.0.1"  # Verify source IP extraction.
    assert summary["dport"] == "80"  # Verify destination port extraction.
