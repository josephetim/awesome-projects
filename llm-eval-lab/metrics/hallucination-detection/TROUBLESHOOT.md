# TROUBLESHOOT

## Model download is slow

- Sentence-transformers and BERTScore models download on first run.
- Keep internet enabled until local cache is created.

## Out-of-memory errors

- Use smaller embedding models.
- Run with CPU-only batch sizes for constrained machines.

## Counterintuitive scores

- Semantic similarity can still score fluent factual errors.
- Inspect examples manually and tune thresholds by domain.
