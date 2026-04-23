"""PostgreSQL persistence for generated briefings."""

from __future__ import annotations

import json  # Import json for serializing source metadata into database column.
import os  # Import os to read database connection string from environment.
from typing import Any  # Import Any for generic row dictionaries.

import psycopg2  # Import psycopg2 for PostgreSQL connectivity.
from dotenv import load_dotenv  # Import dotenv for local environment loading.

load_dotenv()  # Load `.env` values before database operations.


def _database_url() -> str:
    """Return validated database URL."""

    url = os.getenv("DATABASE_URL", "").strip()  # Read database connection URL from environment.
    if not url:  # Validate URL presence to avoid opaque connection failures.
        raise ValueError("Missing DATABASE_URL in environment.")  # Raise actionable setup guidance.
    return url  # Return validated URL string.


def init_db() -> None:
    """Create briefing table if it does not exist."""

    connection = psycopg2.connect(_database_url())  # Open database connection using configured URL.
    try:  # Ensure cleanup happens even when SQL execution fails.
        with connection:  # Use transaction context manager for safe commit/rollback behavior.
            with connection.cursor() as cursor:  # Create cursor for SQL execution.
                cursor.execute(  # Create table for storing generated briefings and metadata.
                    """
                    CREATE TABLE IF NOT EXISTS daily_briefings (
                        id SERIAL PRIMARY KEY,
                        topic TEXT NOT NULL,
                        researcher_notes TEXT NOT NULL,
                        analyst_notes TEXT NOT NULL,
                        briefing TEXT NOT NULL,
                        sources_json TEXT NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );
                    """
                )
    finally:  # Always close connection to release pool/socket resources.
        connection.close()  # Close database connection cleanly.


def save_briefing(topic: str, researcher_notes: str, analyst_notes: str, briefing: str, sources: list[dict]) -> None:
    """Persist one generated briefing record."""

    connection = psycopg2.connect(_database_url())  # Open fresh DB connection for insert operation.
    try:  # Ensure connection closes reliably.
        with connection:  # Wrap insert in transaction context manager.
            with connection.cursor() as cursor:  # Create cursor for SQL statement execution.
                cursor.execute(  # Insert briefing record with serialized source metadata.
                    """
                    INSERT INTO daily_briefings (topic, researcher_notes, analyst_notes, briefing, sources_json)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (topic, researcher_notes, analyst_notes, briefing, json.dumps(sources)),  # Pass values via parameterized query for SQL safety.
                )
    finally:  # Always close connection.
        connection.close()  # Release DB connection resources.


def list_recent_briefings(limit: int = 10) -> list[dict[str, Any]]:
    """Return recent briefing rows ordered by newest first."""

    connection = psycopg2.connect(_database_url())  # Open DB connection for select query.
    try:  # Ensure close on all paths.
        with connection.cursor() as cursor:  # Create cursor for fetch query.
            cursor.execute(  # Query latest briefing records with configurable limit.
                """
                SELECT id, topic, briefing, created_at
                FROM daily_briefings
                ORDER BY created_at DESC
                LIMIT %s;
                """,
                (limit,),  # Parameterize limit value for safe SQL execution.
            )
            rows = cursor.fetchall()  # Fetch all selected rows from cursor.
    finally:  # Ensure connection cleanup.
        connection.close()  # Close DB connection.

    return [  # Convert tuple rows into explicit dictionaries for API/UI consumption.
        {"id": row[0], "topic": row[1], "briefing": row[2], "created_at": str(row[3])}  # Map each column to named key.
        for row in rows
    ]
