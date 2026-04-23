"""Provider adapter for PDF QA chatbot."""

from __future__ import annotations

import os  # Import os to read provider and key environment variables.
from typing import Iterable  # Import Iterable so embedding helper accepts flexible iterables.

from dotenv import load_dotenv  # Import dotenv loader for beginner-friendly local setup.

load_dotenv()  # Load .env variables automatically for local runs.


def _provider() -> str:
    """Return validated provider name."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default provider to Gemini free tier.
    if provider not in {"gemini", "openai"}:  # Restrict adapter to approved provider options only.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear config message for invalid values.
    return provider  # Return validated provider string.


def _require_key(env_name: str) -> str:
    """Read and validate required API key."""

    value = os.getenv(env_name, "").strip()  # Read API key from environment and trim accidental whitespace.
    if not value:  # Fail fast when key is missing to avoid opaque provider SDK errors.
        raise ValueError(f"{env_name} is required for the selected provider.")  # Raise beginner-friendly setup guidance.
    return value  # Return non-empty key value for SDK configuration.


def generate_text(prompt: str, system_prompt: str = "You answer questions using only the provided context.", temperature: float = 0.1, max_tokens: int = 512) -> str:
    """Generate answer text using selected provider."""

    if not prompt.strip():  # Validate prompt before calling external provider endpoints.
        raise ValueError("Prompt cannot be empty.")  # Raise clear input validation error.
    provider = _provider()  # Resolve and validate provider from environment.
    if provider == "gemini":  # Use Gemini branch when free default is selected.
        import google.generativeai as genai  # Import lazily so optional dependencies remain optional.

        genai.configure(api_key=_require_key("GEMINI_API_KEY"))  # Configure Gemini SDK with validated key.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build model from env override or default.
        response = model.generate_content(  # Send system behavior and task prompt as structured content.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide behavior constraints explicitly.
                {"role": "user", "parts": [prompt]},  # Send retrieval prompt containing context and question.
            ],
            generation_config={  # Use deterministic-ish generation settings for grounded answers.
                "temperature": temperature,  # Keep randomness low for QA tasks.
                "max_output_tokens": max_tokens,  # Bound output length for stable UX.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized response text.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    client = OpenAI(api_key=_require_key("OPENAI_API_KEY"))  # Build OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request chat completion using prompt and system constraints.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model name.
        messages=[
            {"role": "system", "content": system_prompt},  # Apply system policy to keep grounded behavior.
            {"role": "user", "content": prompt},  # Send question plus retrieved context.
        ],
        temperature=temperature,  # Keep low randomness for repeatable QA output.
        max_tokens=max_tokens,  # Keep response length controlled.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first-choice response.


def embed_texts(texts: Iterable[str]) -> list[list[float]]:
    """Generate embeddings through selected provider."""

    clean_texts = [text.strip() for text in texts if text and text.strip()]  # Normalize text list and drop empty values.
    if not clean_texts:  # Ensure embedding requests always include at least one real text.
        raise ValueError("embed_texts requires at least one non-empty input string.")  # Raise actionable input validation error.
    provider = _provider()  # Resolve provider for embedding call.
    if provider == "gemini":  # Use Gemini embedding endpoint for free default path.
        import google.generativeai as genai  # Import lazily to avoid hard runtime dependency in non-LLM tests.

        genai.configure(api_key=_require_key("GEMINI_API_KEY"))  # Configure Gemini API client with key.
        model_name = os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004").strip()  # Read embedding model setting.
        vectors: list[list[float]] = []  # Create output vector list with explicit float nesting.
        for text in clean_texts:  # Embed each chunk individually for compatibility with Gemini endpoint.
            result = genai.embed_content(model=model_name, content=text)  # Request embedding vector for one text chunk.
            embedding = result.get("embedding", [])  # Read embedding payload from returned dictionary.
            if not embedding:  # Validate that provider returned a non-empty embedding vector.
                raise RuntimeError("Gemini returned an empty embedding. Please retry.")  # Raise clear retriable error.
            vectors.append([float(value) for value in embedding])  # Coerce values to float for FAISS compatibility.
        return vectors  # Return vectors in same order as input texts.

    from openai import OpenAI  # Import OpenAI lazily to keep optional dependency optional.

    client = OpenAI(api_key=_require_key("OPENAI_API_KEY"))  # Build OpenAI client with validated key.
    result = client.embeddings.create(  # Request embeddings in one batch call for efficiency.
        model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small").strip(),  # Use configurable embedding model.
        input=clean_texts,  # Send normalized text list for embedding.
    )
    return [[float(value) for value in item.embedding] for item in result.data]  # Convert output vectors to plain float lists.
