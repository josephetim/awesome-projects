"""Console entrypoint for networking basics demonstrations."""

from __future__ import annotations

import json  # Import json for readable console output formatting.

from src.networking_basics import dns_lookup, explain_tcp_handshake, http_request_anatomy  # Import educational helper functions.


def main() -> None:
    """Run one safe demo for each networking concept."""

    dns_result = dns_lookup("example.com")  # Demonstrate DNS A record resolution.
    tcp_result = explain_tcp_handshake("example.com", 80)  # Demonstrate TCP handshake explanation and connect test.
    http_result = http_request_anatomy("https://example.com")  # Demonstrate HTTP request anatomy.
    print("DNS Lookup:\n", json.dumps(dns_result, indent=2))  # Print formatted DNS result.
    print("\nTCP Handshake:\n", json.dumps(tcp_result, indent=2))  # Print formatted TCP explanation/result.
    print("\nHTTP Anatomy:\n", json.dumps(http_result, indent=2))  # Print formatted HTTP anatomy output.


if __name__ == "__main__":
    main()  # Execute demo flow when run as script.
