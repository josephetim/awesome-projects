# EXTEND Guide

## Extension Ideas

1. Add hybrid retrieval (dense + keyword).
2. Add query rewriting before retrieval.
3. Add automated weak-score diagnostics and remediation hints.
4. Add versioned experiment tracking for prompt/index settings.

## Practical Advice

- Keep retrieval and evaluation modules decoupled so metric swaps stay easy.
- Monitor score trends over datasets, not just single-question runs.
