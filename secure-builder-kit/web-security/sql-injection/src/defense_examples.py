"""Defensive SQL examples using parameterized queries."""

from __future__ import annotations

import sqlite3  # Import sqlite3 for local parameterized query demonstration.


def safe_lookup_user_by_id(connection: sqlite3.Connection, user_id: int) -> list[tuple]:
    """Run parameterized query to prevent SQL injection."""

    cursor = connection.cursor()  # Create database cursor for query execution.
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))  # Execute parameterized query with positional binding.
    return cursor.fetchall()  # Return fetched rows safely.
