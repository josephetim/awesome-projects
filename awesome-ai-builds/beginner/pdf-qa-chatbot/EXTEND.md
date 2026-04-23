# EXTEND Guide

## Useful Extension Ideas

1. Add citation spans by storing chunk page numbers during PDF extraction.
2. Persist FAISS index to disk so users can reload large PDFs faster.
3. Add multi-file support with per-document source attribution.
4. Add answer evaluation metrics such as groundedness checks.

## Recommended Refactors

- Move UI state into a small class if you add session management.
- Add caching around embedding calls to reduce repeated costs.
