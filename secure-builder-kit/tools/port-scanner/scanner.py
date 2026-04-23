"""CLI for educational TCP port scanner."""

from __future__ import annotations

import argparse  # Import argparse for CLI parsing.

from rich.console import Console  # Import Rich console for readable output.
from rich.table import Table  # Import Rich table for structured result display.

from src.scanner_core import expand_targets, export_csv, export_json, parse_ports, scan_targets  # Import scanner core helpers.

console = Console()  # Create Rich console instance.


def parse_args() -> argparse.Namespace:
    """Parse scanner CLI arguments."""

    parser = argparse.ArgumentParser(description="Authorized-use TCP scanner for defensive labs")  # Create parser with ethics reminder in description.
    parser.add_argument("--target", required=True, help="Single host or CIDR range (for example 192.168.1.0/24)")  # Add required target argument.
    parser.add_argument("--ports", required=True, help="Port list/range, e.g. 22,80,443 or 1-1024")  # Add required port specification argument.
    parser.add_argument("--threads", type=int, default=200, help="Concurrent scan workers")  # Add thread-count argument.
    parser.add_argument("--banner", action="store_true", help="Enable banner grabbing on open ports")  # Add optional banner-grab flag.
    parser.add_argument("--json-out", default="", help="Optional JSON output file path")  # Add optional JSON export argument.
    parser.add_argument("--csv-out", default="", help="Optional CSV output file path")  # Add optional CSV export argument.
    return parser.parse_args()  # Return parsed argument namespace.


def render(rows: list[dict[str, str | int | bool]]) -> None:
    """Render open-port rows in terminal table."""

    table = Table(title="Open Ports")  # Create rich table for result output.
    table.add_column("Host")  # Add host column.
    table.add_column("Port")  # Add port column.
    table.add_column("Banner")  # Add banner column.
    for row in rows:  # Iterate open-port rows.
        table.add_row(str(row["host"]), str(row["port"]), str(row.get("banner", ""))[:80])  # Add row values with banner truncation.
    console.print(table)  # Print final table to terminal.


def main() -> None:
    """Run scanner from CLI args."""

    args = parse_args()  # Parse CLI arguments.
    console.print("[bold yellow]Warning:[/bold yellow] scan only authorized systems.")  # Print ethics warning at runtime.
    targets = expand_targets(args.target)  # Expand target host or CIDR range into host list.
    ports = parse_ports(args.ports)  # Parse port specification into list of port integers.
    results = scan_targets(targets=targets, ports=ports, threads=args.threads, grab_banner=args.banner)  # Run concurrent scan over host/port combinations.
    render(results)  # Display open-port results.
    if args.json_out:  # Export JSON when output path provided.
        export_json(args.json_out, results)  # Write JSON export file.
        console.print(f"JSON exported: {args.json_out}")  # Confirm JSON export.
    if args.csv_out:  # Export CSV when output path provided.
        export_csv(args.csv_out, results)  # Write CSV export file.
        console.print(f"CSV exported: {args.csv_out}")  # Confirm CSV export.


if __name__ == "__main__":
    main()  # Execute CLI workflow when script is run directly.
