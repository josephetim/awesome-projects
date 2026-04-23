"""Celery tasks for background briefing generation."""

from __future__ import annotations

from src.celery_app import celery_app  # Import configured Celery app instance.
from src.news_pipeline import run_multi_agent_pipeline, serper_search  # Import retrieval and agent orchestration pipeline.
from src.storage import init_db, save_briefing  # Import persistence helpers for briefing storage.


@celery_app.task(name="generate_daily_briefing")
def generate_daily_briefing(topic: str) -> dict[str, str]:
    """Generate and persist one daily briefing for a topic."""

    init_db()  # Ensure table exists before attempting insert operation.
    sources = serper_search(topic)  # Retrieve latest sources from Serper for provided topic.
    outputs = run_multi_agent_pipeline(topic=topic, sources=sources)  # Run multi-agent analysis and writing workflow.
    save_briefing(  # Persist generated artifacts to PostgreSQL.
        topic=topic,  # Store topic key for indexing and retrieval.
        researcher_notes=outputs.researcher_notes,  # Store researcher role output for auditability.
        analyst_notes=outputs.analyst_notes,  # Store analyst role output for traceability.
        briefing=outputs.briefing,  # Store final daily briefing text.
        sources=outputs.sources,  # Store source metadata for citation verification.
    )
    return {  # Return concise task summary payload.
        "topic": topic,  # Echo topic for task identification.
        "status": "completed",  # Mark successful completion state.
        "briefing_preview": outputs.briefing[:240],  # Return short preview for logs and CLI feedback.
    }
