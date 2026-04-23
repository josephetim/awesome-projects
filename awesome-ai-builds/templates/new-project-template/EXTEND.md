# EXTEND Guide

## Safe Extension Sequence

1. Add new business logic in `src/` first.
2. Add tests for the new behavior in `tests/`.
3. Expose the behavior through `app.py` or your API route.
4. Update `README.md` inputs/outputs section.
5. Update `architecture.md` data flow if the flow changed.

## Recommended Design Patterns

- Keep I/O code in entrypoint files (`app.py`, `main.py`).
- Keep pure logic in `src/` for easy tests.
- Use small typed functions with clear return values.
