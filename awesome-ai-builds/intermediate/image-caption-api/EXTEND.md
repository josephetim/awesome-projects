# EXTEND Guide

## Useful Extensions

1. Add batch caption endpoint for multiple images in one request.
2. Add optional prompt conditioning for style-specific captions.
3. Add async queueing for heavy model inference workloads.
4. Add response metadata (latency, model version, device).

## Engineering Advice

- Keep model loading cached and separate from route handlers.
- Add integration tests with small fixture images when CI supports model downloads.
