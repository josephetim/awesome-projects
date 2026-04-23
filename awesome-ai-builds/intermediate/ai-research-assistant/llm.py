"""Provider adapter for AI research assistant."""

from __future__ import annotations

import os  # Import os to read provider configuration and model names from environment.

from dotenv import load_dotenv  # Import dotenv so local .env files are loaded automatically.

load_dotenv()  # Load environment values at module import for beginner-friendly local runs.


def _provider() -> str:
    """Return validated provider."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default to Gemini free path when missing.
    if provider not in {"gemini", "openai"}:  # Restrict to approved provider options only.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear validation error for setup mistakes.
    return provider  # Return validated provider string.


def _required(name: str) -> str:
    """Get required env variable with clear message."""

    value = os.getenv(name, "").strip()  # Read and trim env value to avoid whitespace-related issues.
    if not value:  # Ensure required key exists before provider SDK calls.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable configuration guidance.
    return value  # Return non-empty value for runtime use.


def generate_text(prompt: str, system_prompt: str = "You are a rigorous research analyst.", temperature: float = 0.2, max_tokens: int = 900) -> str:
    """Generate text from selected provider."""

    if not prompt.strip():  # Validate input prompt so provider calls are meaningful.
        raise ValueError("Prompt cannot be empty.")  # Raise clear validation error.
    provider = _provider()  # Resolve provider mode from env.
    if provider == "gemini":  # Execute free default Gemini branch.
        import google.generativeai as genai  # Import Gemini SDK lazily to avoid unnecessary dependencies in tests.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini client with validated key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build model using env-configurable name.
        response = model.generate_content(  # Generate response using system instruction plus prompt.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Send behavior constraints in first user turn.
                {"role": "user", "parts": [prompt]},  # Send research synthesis task prompt.
            ],
            generation_config={  # Configure model behavior for balanced detail and determinism.
                "temperature": temperature,  # Keep variability controlled for reproducible summaries.
                "max_output_tokens": max_tokens,  # Allow enough room for structured summary output.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized text response.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Initialize OpenAI client with validated API key.
    completion = client.chat.completions.create(  # Request summary text through chat completion endpoint.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model name with sane default.
        messages=[
            {"role": "system", "content": system_prompt},  # Provide system instruction for research style.
            {"role": "user", "content": prompt},  # Provide prompt containing search evidence.
        ],
        temperature=temperature,  # Keep variance moderate for consistent outputs.
        max_tokens=max_tokens,  # Bound response size for predictable behavior.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first response choice.
