"""Observational networking helpers for educational use."""

from __future__ import annotations

import socket  # Import socket for DNS and TCP connection observations.
from typing import Any  # Import Any for flexible structured return payloads.


def dns_lookup(domain: str) -> dict[str, Any]:
    """Resolve A records for a domain and return structured output."""

    if not domain.strip():  # Validate domain input before DNS resolution.
        raise ValueError("Domain cannot be empty.")  # Raise clear input error for learners.
    import dns.resolver  # Import dnspython resolver lazily so basic tests can run without optional dependency.

    resolver = dns.resolver.Resolver()  # Create DNS resolver instance.
    answers = resolver.resolve(domain.strip(), "A", raise_on_no_answer=False)  # Query A records without raising on empty answer.
    ips = [record.address for record in answers] if answers else []  # Extract resolved IP addresses from DNS answer records.
    return {"domain": domain.strip(), "a_records": ips}  # Return normalized DNS lookup result.


def explain_tcp_handshake(host: str, port: int = 80, timeout: float = 2.0) -> dict[str, Any]:
    """Provide TCP handshake explanation and optional connect test result."""

    steps = [  # Describe handshake phases in plain language.
        "Client sends SYN to server to initiate connection.",  # Step 1 explanation.
        "Server replies with SYN-ACK to acknowledge and synchronize.",  # Step 2 explanation.
        "Client sends ACK to complete handshake and establish session.",  # Step 3 explanation.
    ]
    connect_ok = False  # Initialize connection outcome flag.
    error_message = ""  # Initialize optional error message.
    try:  # Attempt real TCP connection for observational validation.
        with socket.create_connection((host, port), timeout=timeout):  # Open TCP connection with timeout guard.
            connect_ok = True  # Mark successful handshake/connection.
    except OSError as exc:  # Capture connection errors without raising for educational flow.
        error_message = str(exc)  # Store error text for transparent troubleshooting.
    return {  # Return structured handshake explanation and optional live-connect result.
        "host": host,  # Echo target host.
        "port": port,  # Echo target port.
        "steps": steps,  # Include handshake explanation steps.
        "connection_successful": connect_ok,  # Include live connection result.
        "connection_error": error_message,  # Include captured error string when connection fails.
    }


def http_request_anatomy(url: str) -> dict[str, Any]:
    """Send HTTP GET request and return request/response anatomy."""

    if not url.startswith("http://") and not url.startswith("https://"):  # Validate URL scheme for requests compatibility.
        raise ValueError("URL must start with http:// or https://")  # Raise clear validation message.
    import requests  # Import requests lazily so non-HTTP tests can run without optional dependency.

    session = requests.Session()  # Create requests session for consistent request handling.
    request = requests.Request("GET", url)  # Build GET request object.
    prepared = session.prepare_request(request)  # Prepare request to inspect final headers and path.
    response = session.send(prepared, timeout=8)  # Send prepared request with timeout guard.
    return {  # Return request and response anatomy details.
        "request_line": f"{prepared.method} {prepared.path_url} HTTP/1.1",  # Build HTTP request line representation.
        "request_headers": dict(prepared.headers),  # Include sent request headers.
        "status_code": response.status_code,  # Include HTTP status code.
        "response_headers": dict(response.headers),  # Include response headers.
        "response_preview": response.text[:200],  # Include response body preview for quick inspection.
    }
