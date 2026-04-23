"""Shared provider adapter reference for awesome-ai-builds projects."""

from __future__ import annotations

import os  # Import os to read provider and API key environment variables.
from dataclasses import dataclass  # Use dataclass to keep runtime config explicit and typed.
from typing import Iterable  # Import Iterable so embedding helpers can accept flexible text inputs.

from dotenv import load_dotenv  # Load .env values so beginners can run projects without shell exports.

load_dotenv()  # Load environment variables at import time for simple local developer ergonomics.

SUPPORTED_PROVIDERS = {"gemini", "openai"}  # Restrict providers to the two approved options.


@dataclass(frozen=True)
class LLMSettings:
    """Runtime settings for text and embedding calls."""

    provider: str  # Store selected provider so every call follows one clear runtime branch.
    gemini_api_key: str | None  # Keep Gemini key optional because it is only required for Gemini mode.
    openai_api_key: str | None  # Keep OpenAI key optional because it is only required for OpenAI mode.
    gemini_text_model: str  # Hold Gemini text model name so projects can override safely via env.
    gemini_embedding_model: str  # Hold Gemini embedding model name for retrieval projects.
    openai_text_model: str  # Hold OpenAI text model name for optional paid path.
    openai_embedding_model: str  # Hold OpenAI embedding model name for optional paid path.


def _require_env(var_name: str) -> str:
    """Read one required env var and raise a beginner-friendly message when missing."""

    value = os.getenv(var_name, "").strip()  # Read and trim env value so accidental whitespace does not break setup.
    if not value:  # Fail early so users discover misconfiguration before model calls.
        raise ValueError(  # Raise ValueError because this is a user configuration issue.
            f"Missing required environment variable: {var_name}. "  # Name the exact missing variable for quick fixes.
            f"Add it to your .env file and try again."  # Give direct remediation steps.
        )
    return value  # Return validated value for caller use.


def _build_settings() -> LLMSettings:
    """Build and validate provider configuration from environment variables."""

    provider = os.getenv("PROVIDER", "gemini").strip().lower()  # Default provider to Gemini when unset.
    if provider not in SUPPORTED_PROVIDERS:  # Guard against unsupported providers to avoid undefined behavior.
        raise ValueError(  # Raise a clear error that lists valid options.
            "Invalid PROVIDER value. Supported values are 'gemini' and 'openai'."  # Keep message short and exact.
        )

    gemini_key = os.getenv("GEMINI_API_KEY", "").strip() or None  # Allow None when not using Gemini.
    openai_key = os.getenv("OPENAI_API_KEY", "").strip() or None  # Allow None when not using OpenAI.

    if provider == "gemini" and not gemini_key:  # Require Gemini key only for Gemini runtime.
        raise ValueError(  # Raise a beginner-friendly setup message.
            "PROVIDER is set to 'gemini' but GEMINI_API_KEY is missing. "  # Explain mismatch clearly.
            "Get a free Gemini API key and set GEMINI_API_KEY in .env."  # Explain next action and free-tier path.
        )
    if provider == "openai" and not openai_key:  # Require OpenAI key only for OpenAI runtime.
        raise ValueError(  # Raise a beginner-friendly setup message.
            "PROVIDER is set to 'openai' but OPENAI_API_KEY is missing. "  # Explain mismatch clearly.
            "Set OPENAI_API_KEY in .env to use the optional paid OpenAI path."  # Explain upgrade path.
        )

    return LLMSettings(
        provider=provider,  # Persist validated provider value.
        gemini_api_key=gemini_key,  # Persist optional Gemini key.
        openai_api_key=openai_key,  # Persist optional OpenAI key.
        gemini_text_model=os.getenv("GEMINI_TEXT_MODEL", "gemini-1.5-flash").strip(),  # Use fast default Gemini model.
        gemini_embedding_model=os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004").strip(),  # Use strong default embed model.
        openai_text_model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini").strip(),  # Use cost-aware OpenAI text model.
        openai_embedding_model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small").strip(),  # Use efficient OpenAI embed model.
    )


def _normalize_text(value: str) -> str:
    """Normalize generated text and fail clearly when providers return empty payloads."""

    text = value.strip()  # Remove leading/trailing whitespace so downstream code gets clean output.
    if not text:  # Validate non-empty text because empty responses usually indicate provider-side issues.
        raise RuntimeError("The model returned an empty response. Try a clearer prompt and run again.")  # Provide direct recovery advice.
    return text  # Return safe normalized text for caller use.


def generate_text(prompt: str, system_prompt: str = "You are a helpful AI assistant.", temperature: float = 0.2, max_tokens: int = 512) -> str:
    """Generate text using the selected provider."""

    if not prompt.strip():  # Validate input so provider calls are not wasted on blank prompts.
        raise ValueError("Prompt cannot be empty.")  # Raise input validation error for caller feedback.

    settings = _build_settings()  # Build settings at call time so .env edits are picked up without restarts.

    if settings.provider == "gemini":  # Branch into Gemini implementation for the free default.
        import google.generativeai as genai  # Import lazily so non-Gemini projects avoid unnecessary dependency load.

        genai.configure(api_key=settings.gemini_api_key)  # Configure Gemini client with validated key.
        model = genai.GenerativeModel(settings.gemini_text_model)  # Create model instance once per call for simplicity.
        response = model.generate_content(  # Send structured content so system instructions stay explicit.
            [
                {"role": "user", "parts": [f"System instruction: {system_prompt}"]},  # Encode system behavior in first turn.
                {"role": "user", "parts": [prompt]},  # Send user prompt as second turn content.
            ],
            generation_config={  # Use stable generation settings for predictable outputs.
                "temperature": temperature,  # Keep generation controllable for app use cases.
                "max_output_tokens": max_tokens,  # Bound token usage for cost and latency control.
            },
        )
        return _normalize_text(getattr(response, "text", "") or "")  # Normalize response text with guardrails.

    from openai import OpenAI  # Import lazily so Gemini users avoid OpenAI dependency usage.

    client = OpenAI(api_key=settings.openai_api_key)  # Build OpenAI client with validated key.
    completion = client.chat.completions.create(  # Use chat completions for broad compatibility.
        model=settings.openai_text_model,  # Use configured model so users can tune without code edits.
        messages=[
            {"role": "system", "content": system_prompt},  # Send system behavior policy separately.
            {"role": "user", "content": prompt},  # Send user prompt in standard chat format.
        ],
        temperature=temperature,  # Forward caller temperature to control randomness.
        max_tokens=max_tokens,  # Bound output size to keep responses predictable.
    )
    content = completion.choices[0].message.content or ""  # Extract first candidate message safely.
    return _normalize_text(content)  # Normalize output and enforce non-empty responses.


def embed_texts(texts: Iterable[str]) -> list[list[float]]:
    """Generate vector embeddings for one or more texts using the selected provider."""

    text_list = [text.strip() for text in texts if text and text.strip()]  # Normalize and drop empty strings before embedding.
    if not text_list:  # Reject empty input explicitly so retrieval pipelines fail fast with clear errors.
        raise ValueError("embed_texts requires at least one non-empty string.")  # Provide actionable validation message.

    settings = _build_settings()  # Build settings at call time so provider switches apply immediately.

    if settings.provider == "gemini":  # Branch into Gemini embedding path.
        import google.generativeai as genai  # Import lazily to avoid hard dependency on every run.

        genai.configure(api_key=settings.gemini_api_key)  # Configure Gemini with validated API key.
        vectors: list[list[float]] = []  # Create output container with explicit nested float typing.
        for text in text_list:  # Embed each text separately for compatibility with Gemini embed endpoint.
            result = genai.embed_content(model=settings.gemini_embedding_model, content=text)  # Request embedding for one chunk.
            embedding = result.get("embedding", [])  # Pull embedding payload safely from response dictionary.
            if not embedding:  # Guard against malformed API responses before returning vectors.
                raise RuntimeError("Gemini embedding response was empty. Please retry the request.")  # Raise clear retriable error.
            vectors.append([float(value) for value in embedding])  # Coerce values to float for downstream numeric libraries.
        return vectors  # Return dense vectors in input order.

    from openai import OpenAI  # Import lazily so Gemini default remains lightweight.

    client = OpenAI(api_key=settings.openai_api_key)  # Build OpenAI client for embedding requests.
    result = client.embeddings.create(model=settings.openai_embedding_model, input=text_list)  # Embed all texts in one batch for efficiency.
    vectors = [item.embedding for item in result.data]  # Extract embedding arrays from API response objects.
    if len(vectors) != len(text_list):  # Validate one vector per input to prevent silent retrieval corruption.
        raise RuntimeError("Embedding provider returned an unexpected number of vectors.")  # Fail loudly with clear symptom.
    return [[float(value) for value in vector] for vector in vectors]  # Normalize numeric type for FAISS and NumPy workflows.


def provider_name() -> str:
    """Return the active provider for UI labels and debug logs."""

    return os.getenv("PROVIDER", "gemini").strip().lower() or "gemini"  # Expose current provider with Gemini fallback.
