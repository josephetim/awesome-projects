# EXTEND Guide

## Practical Extensions

1. Add per-case latency and token usage budgets.
2. Add weighted scoring where some cases are critical blockers.
3. Add snapshot baselines so regressions are diffed against prior runs.
4. Add CI integration that comments failures in pull requests.

## Design Guidance

- Keep strategies simple and deterministic when possible.
- Reserve LLM-as-judge for nuanced cases where string checks are insufficient.
