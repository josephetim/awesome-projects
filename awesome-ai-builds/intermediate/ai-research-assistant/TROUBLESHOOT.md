# TROUBLESHOOT

## Tavily key errors

- Confirm `TAVILY_API_KEY` is set in `.env`.
- Ensure there are no extra spaces around the key.

## Empty source list

- Some queries may return sparse results.
- Try a more specific question with named entities and timeframe.

## Provider errors

- For Gemini default path, set `GEMINI_API_KEY`.
- For OpenAI mode, set `PROVIDER=openai` and `OPENAI_API_KEY`.

## LangGraph import issues

- Install dependencies with `pip install -r requirements.txt`.
- The project includes a linear fallback if LangGraph is unavailable.
