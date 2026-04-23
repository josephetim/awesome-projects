"""Packet parsing and capture helpers."""

from __future__ import annotations

from typing import Any, Callable  # Import typing helpers for packet summary and callback annotations.


def summarize_packet(packet: Any) -> dict[str, str]:
    """Extract key protocol fields from a packet object."""

    summary = {"protocol": "UNKNOWN", "src": "-", "dst": "-", "sport": "-", "dport": "-"}  # Initialize default summary fields for unknown packets.
    if hasattr(packet, "haslayer") and packet.haslayer("IP"):  # Check for IP layer presence using scapy-like API.
        ip_layer = packet.getlayer("IP")  # Retrieve IP layer for source/destination extraction.
        summary["src"] = str(getattr(ip_layer, "src", "-"))  # Extract source IP address.
        summary["dst"] = str(getattr(ip_layer, "dst", "-"))  # Extract destination IP address.
    if hasattr(packet, "haslayer") and packet.haslayer("TCP"):  # Check for TCP layer.
        tcp_layer = packet.getlayer("TCP")  # Retrieve TCP layer object.
        summary["protocol"] = "TCP"  # Mark protocol as TCP.
        summary["sport"] = str(getattr(tcp_layer, "sport", "-"))  # Extract source port.
        summary["dport"] = str(getattr(tcp_layer, "dport", "-"))  # Extract destination port.
    elif hasattr(packet, "haslayer") and packet.haslayer("UDP"):  # Check for UDP layer when TCP absent.
        udp_layer = packet.getlayer("UDP")  # Retrieve UDP layer object.
        summary["protocol"] = "UDP"  # Mark protocol as UDP.
        summary["sport"] = str(getattr(udp_layer, "sport", "-"))  # Extract source port.
        summary["dport"] = str(getattr(udp_layer, "dport", "-"))  # Extract destination port.
    return summary  # Return structured packet summary.


def capture_packets(iface: str, on_packet: Callable[[Any], None], count: int = 0) -> None:
    """Capture packets on interface and dispatch to callback."""

    from scapy.all import sniff  # Import scapy sniff lazily so tests can run without root capture setup.

    sniff(iface=iface, prn=on_packet, store=False, count=count if count > 0 else 0)  # Start packet capture with callback and optional count limit.
