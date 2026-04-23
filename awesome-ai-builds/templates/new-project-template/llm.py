"""Optional LLM adapter template for projects that call an external model API."""

from __future__ import annotations

import os  # Import os to read provider settings from environment variables.

from dotenv import load_dotenv  # Import dotenv loader so local .env files work without shell exports.

load_dotenv()  # Load environment values before any provider validation.


def generate_text(prompt: str) -> str:
    """Return generated text using either Gemini or OpenAI."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default to Gemini free path when provider is unset.
    if provider not in {"gemini", "openai"}:  # Restrict provider choices to approved values.
        raise ValueError("PROVIDER must be either 'gemini' or 'openai'.")  # Raise clear configuration guidance.
    if not prompt.strip():  # Validate caller input so API calls are not made with blank prompts.
        raise ValueError("Prompt cannot be empty.")  # Raise actionable input error for developers.
    if provider == "gemini":  # Execute Gemini flow when free default is selected.
        import google.generativeai as genai  # Import Gemini SDK lazily to avoid unnecessary package requirements.

        api_key = os.getenv("GEMINI_API_KEY", "").strip()  # Read Gemini key from environment.
        if not api_key:  # Ensure key exists before making provider request.
            raise ValueError("GEMINI_API_KEY is required when PROVIDER=gemini.")  # Explain exactly which variable is missing.
        genai.configure(api_key=api_key)  # Configure SDK client with validated key.
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use fast model by default for developer ergonomics.
        response = model.generate_content(prompt)  # Send prompt and request generated text.
        return (getattr(response, "text", "") or "").strip()  # Return normalized text so callers get clean output.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    api_key = os.getenv("OPENAI_API_KEY", "").strip()  # Read OpenAI key from environment.
    if not api_key:  # Ensure key exists before API call.
        raise ValueError("OPENAI_API_KEY is required when PROVIDER=openai.")  # Provide clear setup error.
    client = OpenAI(api_key=api_key)  # Build OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request a chat completion for the input prompt.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use configurable model name with sane default.
        messages=[{"role": "user", "content": prompt}],  # Pass user prompt as single chat turn.
        temperature=0.2,  # Keep output stable for reproducible project behavior.
        max_tokens=512,  # Bound token output for predictable cost and latency.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first response choice.
