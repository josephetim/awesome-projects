"""Shared provider adapter reference for llm-eval-lab modules."""

from __future__ import annotations

import os  # Import os to read provider configuration from environment.

from dotenv import load_dotenv  # Import dotenv for local `.env` support.

load_dotenv()  # Load environment variables for local development workflows.


def _provider() -> str:
    """Return validated provider name."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default to Gemini free path when unset.
    if provider not in {"gemini", "openai"}:  # Restrict providers to approved options.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear setup error for invalid values.
    return provider  # Return normalized provider string.


def _required(name: str) -> str:
    """Read required env var."""

    value = os.getenv(name, "").strip()  # Read and trim requested env variable.
    if not value:  # Validate non-empty required value.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable config error.
    return value  # Return validated env value.


def generate_text(prompt: str, system_prompt: str = "You are an evaluation assistant.", temperature: float = 0.0, max_tokens: int = 600) -> str:
    """Generate text from selected provider for evaluation workflows."""

    if not prompt.strip():  # Validate prompt before making API request.
        raise ValueError("Prompt cannot be empty.")  # Raise clear input validation error.
    provider = _provider()  # Resolve provider mode from environment.
    if provider == "gemini":  # Execute Gemini branch for free default provider.
        import google.generativeai as genai  # Import Gemini SDK lazily to keep optional dependency optional.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini client using validated key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build model from env-configurable name.
        response = model.generate_content(  # Generate model output from system instruction and prompt.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide evaluation-specific behavior constraints.
                {"role": "user", "parts": [prompt]},  # Provide module prompt payload.
            ],
            generation_config={  # Configure deterministic generation defaults for eval consistency.
                "temperature": temperature,  # Keep randomness low for reproducible scoring behavior.
                "max_output_tokens": max_tokens,  # Bound output length for predictable parsing.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized generated text.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Build OpenAI client using validated key.
    completion = client.chat.completions.create(  # Request completion from selected OpenAI model.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model default.
        messages=[
            {"role": "system", "content": system_prompt},  # Send evaluation behavior constraints.
            {"role": "user", "content": prompt},  # Send prompt payload.
        ],
        temperature=temperature,  # Keep low randomness for stable evaluations.
        max_tokens=max_tokens,  # Bound response length for deterministic parsing.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first completion output.
