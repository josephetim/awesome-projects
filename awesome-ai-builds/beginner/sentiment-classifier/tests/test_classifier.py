"""Tests for sentiment classification logic."""

from src.classifier import classify_sentiment  # Import function under test.


def test_high_confidence_positive_maps_to_positive() -> None:
    """High-confidence POSITIVE should remain positive."""

    result = classify_sentiment("Great release!", raw_result={"label": "POSITIVE", "score": 0.97})  # Inject deterministic model-like result.
    assert result["label"] == "positive"  # Ensure positive mapping is correct.
    assert result["confidence"] == 0.97  # Ensure confidence is preserved for strong predictions.


def test_low_confidence_prediction_maps_to_neutral() -> None:
    """Low-confidence prediction should map to neutral."""

    result = classify_sentiment("It is okay.", raw_result={"label": "NEGATIVE", "score": 0.56})  # Inject low-confidence output to trigger neutral path.
    assert result["label"] == "neutral"  # Ensure uncertain predictions become neutral.
    assert 0.0 <= result["confidence"] <= 1.0  # Ensure neutral confidence stays in valid numeric range.
