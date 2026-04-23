"""Provider adapter for RAGAS pipeline module."""

from __future__ import annotations

import os  # Import os for provider and key environment access.
from typing import Iterable  # Import Iterable for embedding helper input typing.

from dotenv import load_dotenv  # Import dotenv for local `.env` loading.

load_dotenv()  # Load environment variables for local runs.


def _provider() -> str:
    """Validate and return provider."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default to Gemini free path.
    if provider not in {"gemini", "openai"}:  # Restrict to approved providers only.
        raise ValueError("PROVIDER must be 'gemini' or 'openai'.")  # Raise clear setup error.
    return provider  # Return validated provider name.


def _required(name: str) -> str:
    """Read required env var with clear error."""

    value = os.getenv(name, "").strip()  # Read and trim env value.
    if not value:  # Validate non-empty required value.
        raise ValueError(f"Missing required environment variable: {name}")  # Raise actionable setup message.
    return value  # Return validated value.


def generate_text(prompt: str, system_prompt: str = "You are a grounded RAG assistant.", temperature: float = 0.1, max_tokens: int = 700) -> str:
    """Generate answer text via selected provider."""

    if not prompt.strip():  # Validate prompt before provider request.
        raise ValueError("Prompt cannot be empty.")  # Raise clear input error.
    provider = _provider()  # Resolve provider from environment.
    if provider == "gemini":  # Execute free default provider path.
        import google.generativeai as genai  # Import Gemini SDK lazily.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini client.
        model = genai.GenerativeModel(os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip())  # Build model from env config.
        response = model.generate_content(  # Generate output from structured content turns.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Provide system behavior instruction.
                {"role": "user", "parts": [prompt]},  # Provide final prompt with retrieved context.
            ],
            generation_config={  # Configure generation constraints.
                "temperature": temperature,  # Keep randomness low for grounded outputs.
                "max_output_tokens": max_tokens,  # Bound output for consistent evaluation.
            },
        )
        return (getattr(response, "text", "") or "").strip()  # Return normalized response text.

    from openai import OpenAI  # Import OpenAI SDK lazily for optional paid path.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Initialize OpenAI client with validated key.
    completion = client.chat.completions.create(  # Request answer generation completion.
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use env-configurable model.
        messages=[
            {"role": "system", "content": system_prompt},  # Provide grounding behavior constraints.
            {"role": "user", "content": prompt},  # Provide context and question prompt.
        ],
        temperature=temperature,  # Keep variability constrained for reproducibility.
        max_tokens=max_tokens,  # Bound response length.
    )
    return (completion.choices[0].message.content or "").strip()  # Return normalized first completion output.


def embed_texts(texts: Iterable[str]) -> list[list[float]]:
    """Generate embeddings via selected provider."""

    clean_texts = [text.strip() for text in texts if text and text.strip()]  # Normalize embedding inputs and drop empty values.
    if not clean_texts:  # Validate non-empty embedding input set.
        raise ValueError("embed_texts requires at least one non-empty input string.")  # Raise clear input error.
    provider = _provider()  # Resolve provider mode.
    if provider == "gemini":  # Execute Gemini embedding branch.
        import google.generativeai as genai  # Import Gemini SDK lazily.

        genai.configure(api_key=_required("GEMINI_API_KEY"))  # Configure Gemini with validated key.
        model_name = os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004").strip()  # Read Gemini embedding model setting.
        vectors: list[list[float]] = []  # Initialize output vector container.
        for text in clean_texts:  # Iterate over each input string.
            result = genai.embed_content(model=model_name, content=text)  # Request embedding for one text input.
            embedding = result.get("embedding", [])  # Extract embedding values from response dictionary.
            vectors.append([float(value) for value in embedding])  # Normalize embedding values to floats.
        return vectors  # Return Gemini embedding vectors.

    from openai import OpenAI  # Import OpenAI SDK lazily.

    client = OpenAI(api_key=_required("OPENAI_API_KEY"))  # Initialize OpenAI embedding client.
    result = client.embeddings.create(model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small").strip(), input=clean_texts)  # Request batched embeddings.
    return [[float(value) for value in item.embedding] for item in result.data]  # Return normalized embedding vectors.
