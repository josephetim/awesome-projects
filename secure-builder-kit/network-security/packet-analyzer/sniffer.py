"""CLI entrypoint for live packet analyzer."""

from __future__ import annotations

import argparse  # Import argparse for command-line argument parsing.

from rich.console import Console  # Import Rich console for structured terminal output.
from rich.table import Table  # Import Rich table for readable packet summaries.

from src.analyzer import capture_packets, summarize_packet  # Import capture and summary helpers.

console = Console()  # Create global Rich console instance for output rendering.


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description="Educational packet analyzer (authorized use only)")  # Create parser with safety-focused description.
    parser.add_argument("--iface", required=True, help="Network interface to sniff (for example eth0)")  # Add required interface argument.
    parser.add_argument("--count", type=int, default=0, help="Optional packet count limit (0 means continuous)")  # Add optional packet limit argument.
    return parser.parse_args()  # Return parsed CLI arguments.


def render(summary: dict[str, str]) -> None:
    """Render one packet summary row."""

    table = Table(show_header=True, header_style="bold cyan")  # Create rich table with styled header.
    table.add_column("Protocol")  # Add protocol column.
    table.add_column("Source")  # Add source address column.
    table.add_column("Destination")  # Add destination address column.
    table.add_column("Src Port")  # Add source port column.
    table.add_column("Dst Port")  # Add destination port column.
    table.add_row(summary["protocol"], summary["src"], summary["dst"], summary["sport"], summary["dport"])  # Add packet summary row values.
    console.print(table)  # Print table to console.


def main() -> None:
    """Run packet capture loop."""

    args = parse_args()  # Parse CLI options.
    console.print("[bold yellow]Authorized-use only:[/bold yellow] capture traffic only where permitted.")  # Print ethics warning before capture starts.
    capture_packets(args.iface, lambda packet: render(summarize_packet(packet)), count=args.count)  # Start capture and render each summarized packet.


if __name__ == "__main__":
    main()  # Execute CLI flow when script runs directly.
