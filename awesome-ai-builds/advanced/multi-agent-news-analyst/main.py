"""CLI entrypoint for synchronous or queued briefing generation."""

from __future__ import annotations

import argparse  # Import argparse for command-line argument parsing.
import json  # Import json to print readable output payloads.

from src.tasks import generate_daily_briefing  # Import Celery task function for direct or async execution.


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Multi-agent news analyst runner")  # Create argument parser with concise description.
    parser.add_argument("--topic", required=True, help="Topic to monitor and brief")  # Add required topic input argument.
    parser.add_argument("--queue", action="store_true", help="Queue job in Celery instead of running inline")  # Add optional async queue flag.
    return parser.parse_args()  # Return parsed namespace object.


def main() -> None:
    """Run briefing generation in sync or async mode."""

    args = parse_args()  # Parse user CLI flags.
    if args.queue:  # Use asynchronous mode when --queue flag is provided.
        job = generate_daily_briefing.delay(args.topic)  # Enqueue Celery task and return async result handle.
        print(json.dumps({"status": "queued", "task_id": job.id, "topic": args.topic}, indent=2))  # Print queue metadata for operator tracking.
        return  # Exit after queue submission.
    result = generate_daily_briefing(args.topic)  # Execute pipeline synchronously in current process.
    print(json.dumps(result, indent=2))  # Print structured result payload for local CLI usage.


if __name__ == "__main__":
    main()  # Execute CLI flow when file is run directly.
