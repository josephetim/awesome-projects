# Multi-Agent News Analyst

`multi-agent-news-analyst` uses three coordinated agents (Researcher, Analyst, Writer) to produce daily briefings on a topic.

## Why This Exists

Advanced builders need examples of multi-agent orchestration with storage, background jobs, and operational infrastructure.  
This project demonstrates a practical pipeline from retrieval to long-term briefing persistence.

## Skill Level

`advanced`

## Stack

- Python
- CrewAI
- Serper API
- PostgreSQL
- Celery
- Redis
- project-level `llm.py`

## Input and Output

- Input: topic string (for example `"AI regulation in Europe"`)
- Output:
  - research notes
  - trend analysis
  - polished daily briefing
  - persisted record in PostgreSQL

## Provider Setup

- Default free path: `PROVIDER=gemini`
- Optional paid path: `PROVIDER=openai`

## Serper Setup (Free Tier Available)

1. Create account at https://serper.dev/
2. Generate API key from dashboard.
3. Add key to `.env` as `SERPER_API_KEY=...`

Serper provides a free tier suitable for testing and learning.

## Infrastructure Setup

From this project root:

```bash
docker compose up -d
```

This starts:

- PostgreSQL at `localhost:5432`
- Redis at `localhost:6379`

## Run Locally

1. `cd advanced/multi-agent-news-analyst`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Fill required keys and connection URLs
7. Start worker:
   - `celery -A src.tasks.celery_app worker --loglevel=INFO`
8. Run one topic directly:
   - `python main.py --topic "AI chips supply chain"`
9. Queue one topic as background job:
   - `python main.py --topic "AI chips supply chain" --queue`

## Run Tests

- `pytest tests/ -q`

## Notes

- CrewAI path is used when installed; fallback sequential role prompts are included for portability.
- Background execution uses Celery with Redis broker.
