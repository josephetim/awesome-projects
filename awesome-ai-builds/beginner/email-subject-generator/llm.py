"""Provider adapter for email subject generation."""

from __future__ import annotations

import os  # Import os to read provider configuration and API keys.

from dotenv import load_dotenv  # Import dotenv to load local .env files automatically.

load_dotenv()  # Load environment values at import time for beginner-friendly setup.


def _provider() -> str:
    """Return validated provider."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default to Gemini free path when unset.
    if provider not in {"gemini", "openai"}:  # Restrict to supported provider names only.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear config error for invalid provider.
    return provider  # Return validated provider string.


def _required(name: str) -> str:
    """Fetch required env var with a clear error."""

    value = os.getenv(name, "").strip()  # Read and trim env var value.
    if not value:  # Validate presence before provider call.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable setup error.
    return value  # Return validated value.


def generate_text(prompt: str, system_prompt: str = "You are an email copy assistant.", temperature: float = 0.4, max_tokens: int = 400) -> str:
    """Generate text through selected provider."""

    if not prompt.strip():  # Validate prompt before external model call.
        raise ValueError("Prompt cannot be empty.")  # Raise clear input validation error.
    provider = _provider()  # Resolve provider from environment.
    if provider == "gemini":  # Branch to Gemini for free default flow.
        import google.generativeai as genai  # Import Gemini SDK lazily for optional dependency usage.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini client with validated key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build model with env override support.
        response = model.generate_content(  # Send prompt with explicit system behavior context.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Insert behavior guardrails.
                {"role": "user", "parts": [prompt]},  # Insert subject-generation prompt.
            ],
            generation_config={  # Configure generation style for concise subject suggestions.
                "temperature": temperature,  # Keep moderate creativity for varied subject lines.
                "max_output_tokens": max_tokens,  # Bound output size for easier parsing.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized provider output text.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid upgrade path.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Build OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request chat completion for subject generation.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use configurable model with stable default.
        messages=[
            {"role": "system", "content": system_prompt},  # Send system instruction message.
            {"role": "user", "content": prompt},  # Send few-shot task prompt.
        ],
        temperature=temperature,  # Allow creativity while keeping outputs parseable.
        max_tokens=max_tokens,  # Bound token length for stable structured parsing.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first response.
