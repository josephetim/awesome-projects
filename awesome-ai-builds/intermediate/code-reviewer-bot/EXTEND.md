# EXTEND Guide

## Strong Next Steps

1. Add inline review comments mapped to file/line positions.
2. Add review severity levels and auto-labeling.
3. Add duplicate-comment detection to avoid spam.
4. Add allowlist/denylist paths for selective review scope.

## Architecture Advice

- Keep webhook transport concerns in `main.py`.
- Keep GitHub and prompt logic inside `src/reviewer.py`.
