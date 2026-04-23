# EXTEND Guide

## High-Value Extensions

1. Add recurring schedules via Celery Beat for automatic daily topics.
2. Add confidence scoring per claim with source-level traceability.
3. Add multi-topic portfolio mode with per-topic briefing retention policies.
4. Add alerting hooks (Slack/Email) when briefing risk section exceeds threshold.

## Engineering Guidance

- Keep each agent role prompt small and explicit.
- Store role outputs separately for auditability and iterative prompt tuning.
