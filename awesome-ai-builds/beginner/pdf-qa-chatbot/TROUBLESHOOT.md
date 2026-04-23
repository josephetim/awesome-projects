# TROUBLESHOOT

## `No extractable text was found in this PDF`

- Your PDF may be image-only.
- Run OCR first, then upload the OCR-enabled PDF.

## `faiss` installation errors

- Use Python 3.10+ and install from `requirements.txt`.
- On CPU-only systems, keep `faiss-cpu`.

## Empty or weak answers

- Ask specific questions tied to concrete terms in the PDF.
- Re-index after changing `chunk_size` or `chunk_overlap`.
- Confirm API key is valid for the selected provider.

## Provider errors

- Ensure `.env` contains `PROVIDER=gemini` or `PROVIDER=openai`.
- For Gemini: set `GEMINI_API_KEY`.
- For OpenAI: set `OPENAI_API_KEY`.
