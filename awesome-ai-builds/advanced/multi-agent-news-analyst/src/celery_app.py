"""Celery application configuration."""

from __future__ import annotations

import os  # Import os to read Redis broker URL from environment.

from celery import Celery  # Import Celery for asynchronous task orchestration.
from dotenv import load_dotenv  # Import dotenv to load `.env` config values.

load_dotenv()  # Load environment variables before Celery app initialization.

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0").strip()  # Resolve Redis URL with local default fallback.

celery_app = Celery("news_analyst", broker=redis_url, backend=redis_url)  # Create Celery app using Redis for broker and backend.
celery_app.conf.update(  # Configure Celery runtime behavior.
    task_serializer="json",  # Serialize task payloads as JSON for readability and interoperability.
    accept_content=["json"],  # Restrict accepted content types for safety and predictability.
    result_serializer="json",  # Serialize task results as JSON.
    timezone="UTC",  # Use UTC for consistent cross-region scheduling behavior.
    enable_utc=True,  # Ensure UTC mode is enforced in worker runtime.
)
