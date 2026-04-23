"""Provider adapter for prompt regression module."""

from __future__ import annotations

import os  # Import os to read provider and API key environment variables.

from dotenv import load_dotenv  # Import dotenv to support local `.env` files.

load_dotenv()  # Load environment variables at import time for local developer convenience.


def _provider() -> str:
    """Validate provider setting."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default provider to Gemini when unset.
    if provider not in {"gemini", "openai"}:  # Restrict to approved providers.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear setup error for invalid provider values.
    return provider  # Return validated provider.


def _required(name: str) -> str:
    """Read required env var."""

    value = os.getenv(name, "").strip()  # Read and normalize requested env value.
    if not value:  # Validate non-empty value before API calls.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable error message.
    return value  # Return validated env value.


def generate_text(prompt: str, system_prompt: str = "You are an evaluation assistant.", temperature: float = 0.0, max_tokens: int = 400) -> str:
    """Generate text for prompt tests."""

    if not prompt.strip():  # Validate prompt input before sending to provider.
        raise ValueError("Prompt cannot be empty.")  # Raise clear caller error on invalid input.
    provider = _provider()  # Resolve provider from environment.
    if provider == "gemini":  # Execute Gemini free default flow.
        import google.generativeai as genai  # Import Gemini SDK lazily.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini with validated key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build Gemini model from env config.
        response = model.generate_content(  # Generate output with explicit system behavior.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide system instruction.
                {"role": "user", "parts": [prompt]},  # Provide prompt case input.
            ],
            generation_config={  # Configure deterministic generation for repeatable tests.
                "temperature": temperature,  # Keep randomness low for regression stability.
                "max_output_tokens": max_tokens,  # Bound output size for easier evaluation.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized generated text.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Initialize OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request chat completion for case prompt.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model default.
        messages=[
            {"role": "system", "content": system_prompt},  # Provide system behavior message.
            {"role": "user", "content": prompt},  # Provide case prompt message.
        ],
        temperature=temperature,  # Keep deterministic generation for regression tests.
        max_tokens=max_tokens,  # Keep output bounded.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first completion choice.
