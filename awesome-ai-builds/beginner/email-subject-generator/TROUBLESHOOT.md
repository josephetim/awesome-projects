# TROUBLESHOOT

## API key errors

- Verify `.env` exists in this project folder.
- For Gemini default: set `GEMINI_API_KEY`.
- For OpenAI mode: set `OPENAI_API_KEY` and `PROVIDER=openai`.

## Invalid JSON output from model

- The parser includes fallback handling for lists, but better results come from explicit prompts.
- Keep email body focused and avoid mixing multiple unrelated threads.

## Streamlit does not launch

- Ensure virtual environment is active.
- Run `python app.py` from this project root directory.
