# TROUBLESHOOT

## `Missing SERPER_API_KEY`

- Add `SERPER_API_KEY` to `.env`.
- Confirm key is active in Serper dashboard.

## Celery jobs not running

- Ensure Redis is running (`docker compose up -d`).
- Start worker: `celery -A src.tasks.celery_app worker --loglevel=INFO`.

## Database connection errors

- Verify PostgreSQL container is healthy and `DATABASE_URL` is correct.
- Ensure local firewall/network allows `localhost:5432`.

## Empty briefings

- Check Serper result quality for your topic.
- Use narrower topic wording with explicit entities and timeframe.
