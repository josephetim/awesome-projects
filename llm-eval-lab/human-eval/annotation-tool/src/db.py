"""SQLite persistence helpers for annotation tool."""

from __future__ import annotations

import os  # Import os to resolve DB path from environment.
import sqlite3  # Import sqlite3 for local embedded database storage.
from contextlib import closing  # Import closing for safe connection cleanup.
from typing import Any  # Import Any for generic row dictionaries.

from dotenv import load_dotenv  # Import dotenv for local `.env` support.

load_dotenv()  # Load DB path config from `.env`.


def _db_path() -> str:
    """Return configured SQLite file path."""

    return os.getenv("DB_PATH", "annotation.db").strip() or "annotation.db"  # Return env path with safe default fallback.


def get_connection() -> sqlite3.Connection:
    """Create SQLite connection with row dict-like access."""

    connection = sqlite3.connect(_db_path())  # Open SQLite connection to configured file path.
    connection.row_factory = sqlite3.Row  # Enable dict-like row access for readability.
    return connection  # Return configured connection object.


def init_db() -> None:
    """Initialize tables and seed sample items."""

    with closing(get_connection()) as connection:  # Open connection and ensure closure.
        with connection:  # Use transaction context for atomic schema setup.
            connection.execute(  # Create items table for annotation targets.
                """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    output TEXT NOT NULL
                );
                """
            )
            connection.execute(  # Create annotations table for annotator ratings.
                """
                CREATE TABLE IF NOT EXISTS annotations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    annotator TEXT NOT NULL,
                    relevance INTEGER NOT NULL,
                    accuracy INTEGER NOT NULL,
                    tone INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items(id)
                );
                """
            )
            count = connection.execute("SELECT COUNT(*) AS c FROM items").fetchone()["c"]  # Count existing items to avoid duplicate seeding.
            if count == 0:  # Seed demo items only when table is empty.
                connection.executemany(  # Insert sample prompt/output items for immediate annotation usage.
                    "INSERT INTO items (prompt, output) VALUES (?, ?)",
                    [
                        ("Explain zero-trust security in one paragraph.", "Zero-trust security assumes no implicit trust and continuously verifies users and devices."),
                        ("Summarize why input validation matters.", "Input validation reduces injection risks and prevents malformed data from reaching sensitive logic."),
                        ("How should an assistant handle harmful requests?", "An assistant should refuse unsafe instructions and offer safer alternatives."),
                    ],
                )


def list_items() -> list[dict[str, Any]]:
    """Return all annotation target items."""

    with closing(get_connection()) as connection:  # Open connection for read query.
        rows = connection.execute("SELECT id, prompt, output FROM items ORDER BY id").fetchall()  # Fetch all items ordered by ID.
    return [dict(row) for row in rows]  # Convert row objects to plain dictionaries.


def get_item(item_id: int) -> dict[str, Any] | None:
    """Return one item by ID."""

    with closing(get_connection()) as connection:  # Open connection for read query.
        row = connection.execute("SELECT id, prompt, output FROM items WHERE id = ?", (item_id,)).fetchone()  # Fetch item row by ID.
    return dict(row) if row else None  # Return dictionary when found, else None.


def add_annotation(item_id: int, annotator: str, relevance: int, accuracy: int, tone: int) -> None:
    """Insert annotation record."""

    with closing(get_connection()) as connection:  # Open connection for insert query.
        with connection:  # Use transaction context for insert commit.
            connection.execute(  # Insert one annotation record with rubric ratings.
                """
                INSERT INTO annotations (item_id, annotator, relevance, accuracy, tone)
                VALUES (?, ?, ?, ?, ?)
                """,
                (item_id, annotator.strip(), relevance, accuracy, tone),  # Bind validated annotation values.
            )


def list_annotations() -> list[dict[str, Any]]:
    """Return all annotations with item metadata."""

    with closing(get_connection()) as connection:  # Open connection for join query.
        rows = connection.execute(  # Fetch annotations joined with item prompts for results page context.
            """
            SELECT a.id, a.item_id, a.annotator, a.relevance, a.accuracy, a.tone, a.created_at, i.prompt
            FROM annotations a
            JOIN items i ON i.id = a.item_id
            ORDER BY a.created_at DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]  # Convert rows to dictionaries for template rendering.
