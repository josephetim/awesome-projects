"""Provider adapter for model comparison dashboard."""

from __future__ import annotations

import os  # Import os for provider and API key environment access.

from dotenv import load_dotenv  # Import dotenv for local `.env` loading.

load_dotenv()  # Load environment variables at import time for local usability.


def _resolve_provider(provider: str | None = None) -> str:
    """Resolve provider argument or fallback env provider."""

    resolved = (provider or os.getenv("PROVIDER", "gemini")).strip().lower()  # Use explicit provider when passed, else default to env Gemini fallback.
    if resolved not in {"gemini", "openai"}:  # Restrict to approved providers only.
        raise ValueError("Provider must be 'gemini' or 'openai'.")  # Raise clear validation error.
    return resolved  # Return validated provider label.


def _required(name: str) -> str:
    """Read required env var."""

    value = os.getenv(name, "").strip()  # Read and normalize env variable.
    if not value:  # Validate required value presence.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable setup error.
    return value  # Return validated value.


def generate_text(prompt: str, provider: str | None = None, system_prompt: str = "You are a benchmark assistant.", temperature: float = 0.2, max_tokens: int = 500) -> str:
    """Generate text using selected provider."""

    if not prompt.strip():  # Validate prompt before API call.
        raise ValueError("Prompt cannot be empty.")  # Raise clear input validation error.
    resolved = _resolve_provider(provider)  # Resolve provider with optional override.
    if resolved == "gemini":  # Execute Gemini branch.
        import google.generativeai as genai  # Import Gemini SDK lazily.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini client with validated key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Initialize Gemini model from env config.
        response = model.generate_content(  # Request response with explicit behavior instruction.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide behavior instruction.
                {"role": "user", "parts": [prompt]},  # Provide benchmark prompt.
            ],
            generation_config={  # Configure output behavior.
                "temperature": temperature,  # Keep variability moderate for realistic outputs.
                "max_output_tokens": max_tokens,  # Bound output length for fair scoring.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized output text.

    from openai import OpenAI  # Import OpenAI SDK lazily.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Initialize OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request OpenAI completion for benchmark prompt.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model name.
        messages=[
            {"role": "system", "content": system_prompt},  # Provide behavior instruction.
            {"role": "user", "content": prompt},  # Provide benchmark prompt.
        ],
        temperature=temperature,  # Keep output variability moderate.
        max_tokens=max_tokens,  # Bound response size for scoring consistency.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first response choice.
