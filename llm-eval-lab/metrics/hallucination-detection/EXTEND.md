# EXTEND Guide

## High-Impact Extensions

1. Add claim-level extraction and claim-level grounding checks.
2. Add threshold tuning per domain (legal, medical, coding).
3. Add calibration plots comparing scores with human labels.
4. Add batch CLI for evaluating large datasets.

## Practical Advice

- Use lexical scores for quick triage and semantic scores for deeper validation.
- Always validate metric decisions with sampled human review.
