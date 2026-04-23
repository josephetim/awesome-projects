"""Tests for bias audit disparity scoring."""

from src.bias_audit import disparity_score, tone_score  # Import functions under test.


def test_tone_score_increases_with_positive_language() -> None:
    """Positive language should produce higher tone score."""

    positive = "The candidate is strong, capable, and highly qualified."  # Define positive sample output.
    negative = "The candidate is weak and unsuitable for the role."  # Define negative sample output.
    assert tone_score(positive) > tone_score(negative)  # Verify heuristic tone scoring direction.


def test_disparity_score_zero_for_identical_outputs() -> None:
    """Identical outputs should yield zero disparity."""

    text = "The candidate is qualified and reliable."  # Define identical output text for both variants.
    assert disparity_score(text, text) == 0.0  # Ensure no disparity is reported for identical outputs.
