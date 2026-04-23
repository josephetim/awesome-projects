"""Provider adapter for bias audit module."""

from __future__ import annotations

import os  # Import os for environment-based provider and API key access.

from dotenv import load_dotenv  # Import dotenv for local `.env` loading.

load_dotenv()  # Load environment variables at import time.


def _resolve_provider(provider: str | None = None) -> str:
    """Resolve explicit provider or fallback env provider."""

    resolved = (provider or os.getenv("PROVIDER", "gemini")).strip().lower()  # Use explicit provider override or default env value.
    if resolved not in {"gemini", "openai"}:  # Restrict providers to approved options.
        raise ValueError("Provider must be 'gemini' or 'openai'.")  # Raise clear validation error.
    return resolved  # Return validated provider.


def _required(name: str) -> str:
    """Read required env variable."""

    value = os.getenv(name, "").strip()  # Read and normalize env var.
    if not value:  # Validate required key presence.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable setup error.
    return value  # Return validated key.


def generate_text(prompt: str, provider: str | None = None, system_prompt: str = "You are a fair and neutral assistant.", temperature: float = 0.2, max_tokens: int = 450) -> str:
    """Generate text with selected provider."""

    if not prompt.strip():  # Validate prompt before provider call.
        raise ValueError("Prompt cannot be empty.")  # Raise clear input validation error.
    resolved = _resolve_provider(provider)  # Resolve provider name.
    if resolved == "gemini":  # Execute Gemini branch.
        import google.generativeai as genai  # Import Gemini SDK lazily.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini with validated key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Create Gemini model from env setting.
        response = model.generate_content(  # Generate output for audit prompt.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide neutral behavior instruction.
                {"role": "user", "parts": [prompt]},  # Provide audit prompt content.
            ],
            generation_config={  # Configure generation behavior.
                "temperature": temperature,  # Keep moderate variability for natural responses.
                "max_output_tokens": max_tokens,  # Bound response length for fair scoring.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized response text.

    from openai import OpenAI  # Import OpenAI SDK lazily.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Initialize OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request output generation for audit prompt.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model name.
        messages=[
            {"role": "system", "content": system_prompt},  # Provide neutral behavior instruction.
            {"role": "user", "content": prompt},  # Provide audit prompt content.
        ],
        temperature=temperature,  # Keep moderate variation.
        max_tokens=max_tokens,  # Bound output size.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first completion output.
