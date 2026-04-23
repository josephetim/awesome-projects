"""Core scanning logic for educational TCP port scanner."""

from __future__ import annotations

import csv  # Import csv for export helper.
import ipaddress  # Import ipaddress for CIDR expansion.
import json  # Import json for JSON export helper.
import socket  # Import socket for low-level TCP connection attempts.
from concurrent.futures import ThreadPoolExecutor, as_completed  # Import thread pool utilities for concurrent scanning.
from typing import Iterable  # Import Iterable typing helper.


def expand_targets(target: str) -> list[str]:
    """Expand single host or CIDR string into host list."""

    if "/" not in target:  # Detect single-host input.
        return [target.strip()]  # Return single normalized target host list.
    network = ipaddress.ip_network(target.strip(), strict=False)  # Parse CIDR network definition.
    return [str(host) for host in network.hosts()]  # Return all host IPs in CIDR range.


def parse_ports(port_spec: str) -> list[int]:
    """Parse comma-separated ports and ranges into sorted unique list."""

    ports: set[int] = set()  # Initialize unique port set for deduplicated results.
    for chunk in port_spec.split(","):  # Iterate over comma-separated chunks.
        part = chunk.strip()  # Normalize chunk spacing.
        if not part:  # Skip empty chunks.
            continue  # Continue to next chunk.
        if "-" in part:  # Handle range chunk.
            start_s, end_s = part.split("-", maxsplit=1)  # Split range into start/end strings.
            start = int(start_s)  # Parse range start port.
            end = int(end_s)  # Parse range end port.
            for port in range(min(start, end), max(start, end) + 1):  # Expand inclusive range regardless of order.
                if 1 <= port <= 65535:  # Keep only valid TCP port numbers.
                    ports.add(port)  # Add valid port to set.
        else:  # Handle single port chunk.
            port = int(part)  # Parse individual port.
            if 1 <= port <= 65535:  # Validate port bounds.
                ports.add(port)  # Add valid port.
    return sorted(ports)  # Return sorted list for deterministic scan order.


def scan_port(host: str, port: int, timeout: float = 0.8, grab_banner: bool = False) -> dict[str, str | int | bool]:
    """Scan one TCP port and optionally grab service banner."""

    banner = ""  # Initialize banner value.
    is_open = False  # Initialize open-port flag.
    # TCP handshake note: connect() performs SYN/SYN-ACK/ACK under the hood when a port is open.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # Create TCP socket for one connection probe.
        sock.settimeout(timeout)  # Set timeout so closed/filtered ports do not stall scans.
        if sock.connect_ex((host, port)) == 0:  # Check open state by testing TCP connect result code.
            is_open = True  # Mark port open when connect succeeds.
            if grab_banner:  # Optionally collect service banner for fingerprinting.
                try:  # Guard banner read with exception handling for silent services.
                    sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")  # Send lightweight probe request that many services safely ignore/respond to.
                    banner = sock.recv(128).decode("utf-8", errors="ignore").strip()  # Read and decode small banner sample.
                except OSError:  # Ignore banner errors to keep scanning robust.
                    banner = ""  # Leave banner empty when read fails.
    return {"host": host, "port": port, "open": is_open, "banner": banner}  # Return structured scan result row.


def scan_targets(targets: Iterable[str], ports: Iterable[int], threads: int = 200, grab_banner: bool = False) -> list[dict[str, str | int | bool]]:
    """Scan many hosts/ports concurrently."""

    results: list[dict[str, str | int | bool]] = []  # Initialize output result list.
    with ThreadPoolExecutor(max_workers=max(1, threads)) as pool:  # Create bounded thread pool for concurrent I/O scanning.
        futures = [pool.submit(scan_port, host, port, 0.8, grab_banner) for host in targets for port in ports]  # Submit host/port scan tasks to thread pool.
        # Threading note: network scans are I/O-bound, so concurrency improves throughput by overlapping socket waits.
        for future in as_completed(futures):  # Process results as soon as each task finishes.
            row = future.result()  # Retrieve finished scan result row.
            if row["open"]:  # Keep only open-port rows to reduce noise.
                results.append(row)  # Append open-port result row.
    return sorted(results, key=lambda row: (str(row["host"]), int(row["port"])))  # Return results sorted by host/port for stable output.


def export_json(path: str, rows: list[dict[str, str | int | bool]]) -> None:
    """Export scan rows to JSON file."""

    with open(path, "w", encoding="utf-8") as handle:  # Open output file for JSON writing.
        json.dump(rows, handle, indent=2)  # Write formatted JSON payload.


def export_csv(path: str, rows: list[dict[str, str | int | bool]]) -> None:
    """Export scan rows to CSV file."""

    with open(path, "w", newline="", encoding="utf-8") as handle:  # Open output file for CSV writing.
        writer = csv.DictWriter(handle, fieldnames=["host", "port", "open", "banner"])  # Create CSV writer with stable column order.
        writer.writeheader()  # Write CSV header row.
        writer.writerows(rows)  # Write all result rows.
