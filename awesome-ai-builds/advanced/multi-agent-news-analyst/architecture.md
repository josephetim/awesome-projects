# Architecture

This project orchestrates retrieval, role-based reasoning, and persistence through a background-job pipeline.

## Data Flow

```mermaid
flowchart LR
  A["Topic Input"] --> B["Celery Task: generate_daily_briefing"]
  B --> C["Serper Search Retrieval"]
  C --> D["Researcher Agent"]
  D --> E["Analyst Agent"]
  E --> F["Writer Agent"]
  F --> G["PostgreSQL Storage"]
  B --> H["Redis Broker/Backend"]
```

The task worker pulls a topic from Redis-backed Celery queues, retrieves sources, runs role-specific reasoning, and stores final outputs in PostgreSQL.
