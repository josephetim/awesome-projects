# TROUBLESHOOT

## Empty retrieval context

- Ensure `data/*.txt` files exist and are non-empty.
- Reduce chunk size if retrieval misses key details.

## Low faithfulness scores

- Strengthen grounding instruction in prompt.
- Increase retrieval `top_k` to include more evidence.

## RAGAS import/runtime errors

- Install dependencies from `requirements.txt`.
- The pipeline includes local heuristic fallback when RAGAS is unavailable.
