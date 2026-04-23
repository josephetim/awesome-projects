"""Provider adapter for multi-agent news analyst."""

from __future__ import annotations

import os  # Import os to access provider configuration from environment variables.

from dotenv import load_dotenv  # Import dotenv to load local `.env` configuration.

load_dotenv()  # Load environment variables at module import for easy local setup.


def _provider() -> str:
    """Resolve and validate provider."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default to Gemini free path when provider is not set.
    if provider not in {"gemini", "openai"}:  # Restrict options to approved provider set.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear configuration error for invalid value.
    return provider  # Return validated provider value.


def _required(name: str) -> str:
    """Read required env var with clear errors."""

    value = os.getenv(name, "").strip()  # Read environment value and trim spaces.
    if not value:  # Validate non-empty value before using it in SDK calls.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable setup guidance.
    return value  # Return validated value.


def generate_text(prompt: str, system_prompt: str = "You are a precise analyst.", temperature: float = 0.2, max_tokens: int = 1200) -> str:
    """Generate text through selected provider."""

    if not prompt.strip():  # Validate prompt to avoid empty model requests.
        raise ValueError("Prompt cannot be empty.")  # Raise input validation error.
    provider = _provider()  # Resolve provider mode from environment.
    if provider == "gemini":  # Execute free default provider branch.
        import google.generativeai as genai  # Import Gemini SDK lazily for optional dependency usage.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini client with validated API key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build model from env-configurable name.
        response = model.generate_content(  # Generate output from system instruction and prompt.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide behavioral constraints.
                {"role": "user", "parts": [prompt]},  # Provide current role task prompt.
            ],
            generation_config={  # Configure generation behavior.
                "temperature": temperature,  # Keep output stable for repeatable pipeline behavior.
                "max_output_tokens": max_tokens,  # Allow enough tokens for analysis and briefing composition.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized generated text.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Initialize OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request completion for role-specific agent task.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model with sensible default.
        messages=[
            {"role": "system", "content": system_prompt},  # Provide role-specific behavior constraints.
            {"role": "user", "content": prompt},  # Provide agent task prompt.
        ],
        temperature=temperature,  # Keep randomness controlled for production-grade consistency.
        max_tokens=max_tokens,  # Bound output length for predictable task runtime.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first response text.
