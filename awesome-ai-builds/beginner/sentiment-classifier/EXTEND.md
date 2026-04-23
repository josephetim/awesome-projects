# EXTEND Guide

## Recommended Extensions

1. Add multilingual sentiment using a multilingual transformer model.
2. Add batched inference for CSV inputs.
3. Add calibration charts to evaluate confidence reliability.

## Design Notes

- Keep label mapping and threshold logic in `src/classifier.py`.
- Keep UI concerns in `app.py` only.
