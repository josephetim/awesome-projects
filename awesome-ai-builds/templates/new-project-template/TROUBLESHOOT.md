# TROUBLESHOOT

## Import Errors

- Confirm dependencies are installed: `pip install -r requirements.txt`.
- Run commands from this project root so `src/` imports resolve correctly.

## Test Failures

- Run `pytest tests/ -q` to isolate failure output.
- Verify your new logic did not change expected test behavior.

## Environment Errors

- Ensure `.env` exists when your project uses provider-based LLM calls.
- Confirm `PROVIDER` is either `gemini` or `openai`.
