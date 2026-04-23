"""Provider adapter for code reviewer bot."""

from __future__ import annotations

import os  # Import os for environment-based provider and key configuration.

from dotenv import load_dotenv  # Import dotenv to load .env values automatically.

load_dotenv()  # Load environment variables for local runtime convenience.


def _provider() -> str:
    """Return validated provider value."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default to Gemini when provider is unset.
    if provider not in {"gemini", "openai"}:  # Restrict to approved provider options.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear config error for invalid values.
    return provider  # Return validated provider string.


def _required(name: str) -> str:
    """Get required env var."""

    value = os.getenv(name, "").strip()  # Read and trim env value.
    if not value:  # Validate presence of required key.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable setup error.
    return value  # Return validated env value.


def generate_text(prompt: str, system_prompt: str = "You are a senior software reviewer.", temperature: float = 0.2, max_tokens: int = 900) -> str:
    """Generate review text via selected provider."""

    if not prompt.strip():  # Validate prompt before model request.
        raise ValueError("Prompt cannot be empty.")  # Raise clear validation error for callers.
    provider = _provider()  # Resolve provider from environment.
    if provider == "gemini":  # Handle Gemini free default path.
        import google.generativeai as genai  # Import Gemini SDK lazily.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini SDK using required key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build model from configurable name.
        response = model.generate_content(  # Generate review using system behavior and task prompt.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide behavior constraints as instruction.
                {"role": "user", "parts": [prompt]},  # Provide diff-based review task prompt.
            ],
            generation_config={  # Set deterministic-ish generation params.
                "temperature": temperature,  # Keep output stable for review consistency.
                "max_output_tokens": max_tokens,  # Bound output length for comment readability.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized generated review text.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Build OpenAI client using required key.
    completion = client.chat.completions.create(  # Request structured review text from OpenAI chat model.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model name with sensible default.
        messages=[
            {"role": "system", "content": system_prompt},  # Provide review style and quality constraints.
            {"role": "user", "content": prompt},  # Provide pull request metadata and diff text.
        ],
        temperature=temperature,  # Keep response variance low for reliable structure.
        max_tokens=max_tokens,  # Limit output size for practical PR comment length.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first-choice output.
