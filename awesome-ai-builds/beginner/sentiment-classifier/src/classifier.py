"""Local sentiment analysis utilities."""

from __future__ import annotations

from functools import lru_cache  # Cache model pipeline so app calls do not reload weights repeatedly.
from typing import Any  # Use Any for flexible typing of transformer output dictionaries.


@lru_cache(maxsize=1)
def load_pipeline() -> Any:
    """Load and cache Hugging Face sentiment pipeline."""

    from transformers import pipeline  # Import lazily so tests can run logic without loading heavy model dependencies.

    return pipeline(  # Return pre-configured sentiment pipeline for local inference.
        task="sentiment-analysis",  # Use sentiment-analysis task to get polarity labels and confidence scores.
        model="distilbert-base-uncased-finetuned-sst-2-english",  # Select lightweight and reliable default sentiment model.
    )


def _neutral_confidence(score: float) -> float:
    """Compute confidence for neutral classification based on distance from decision boundary."""

    confidence = max(0.0, 1.0 - abs(score - 0.5) * 2.0)  # Convert closeness-to-boundary into neutral confidence between 0 and 1.
    return round(confidence, 4)  # Round to stable decimals for readable UI output.


def classify_sentiment(text: str, neutral_threshold: float = 0.65, raw_result: dict[str, Any] | None = None) -> dict[str, Any]:
    """Classify text into positive, negative, or neutral with confidence."""

    if not text.strip():  # Validate input so model is not called with empty content.
        raise ValueError("Input text cannot be empty.")  # Raise clear input guidance for app layer.

    result = raw_result if raw_result is not None else load_pipeline()(text)[0]  # Use injected result in tests or model inference in runtime.
    model_label = str(result.get("label", "")).upper().strip()  # Normalize model label for robust mapping logic.
    score = float(result.get("score", 0.0))  # Convert confidence score to float for deterministic branching.

    if score < neutral_threshold:  # Treat low-confidence polarity predictions as neutral to support three-class output.
        return {  # Return neutral label with boundary-based confidence explanation score.
            "label": "neutral",  # Map uncertain sentiment to neutral category.
            "confidence": _neutral_confidence(score),  # Expose neutral confidence derived from uncertainty.
            "raw_label": model_label.lower(),  # Include original model label for debugging and transparency.
            "raw_score": round(score, 4),  # Include raw model score for inspection.
        }

    label = "positive" if model_label == "POSITIVE" else "negative"  # Map binary model output to human-readable project labels.
    return {  # Return final classification dictionary used directly by UI layer.
        "label": label,  # Return mapped sentiment class.
        "confidence": round(score, 4),  # Return rounded confidence for readable display.
        "raw_label": model_label.lower(),  # Return original label for transparency.
        "raw_score": round(score, 4),  # Return original score for transparency.
    }
