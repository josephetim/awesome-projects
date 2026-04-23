"""Simple local checks for expected lab endpoints."""

from __future__ import annotations

import socket  # Import socket for lightweight TCP reachability checks.


def is_port_open(host: str, port: int, timeout: float = 1.5) -> bool:
    """Return True when TCP port is reachable."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # Create TCP socket for reachability test.
        sock.settimeout(timeout)  # Set timeout to avoid hanging when host is unreachable.
        return sock.connect_ex((host, port)) == 0  # Return True when connect call succeeds.
