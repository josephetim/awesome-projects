# TROUBLESHOOT

## One provider fails during benchmark

- Confirm the corresponding API key exists in `.env`.
- Run single-provider benchmarks temporarily for diagnosis.

## Scores look too similar

- Increase prompt diversity across categories.
- Add tougher tasks and edge cases to the prompt dataset.

## Slow dashboard runs

- Reduce prompt set size during iteration.
- Cache benchmark results between UI reruns.
