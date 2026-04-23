# EXTEND Guide

## Recommended Extensions

1. Add iterative query refinement when initial search confidence is low.
2. Add source deduplication and domain diversity constraints.
3. Add export options (Markdown, PDF, JSON).
4. Add evaluation checks for citation-grounded claims.

## Technical Guidance

- Keep external tools behind injectable function interfaces for easier tests.
- Keep synthesis prompt format stable so downstream parsing remains reliable.
