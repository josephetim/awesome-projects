"""Tests for local grounding metric helpers."""

from src.hallucination import normalize_text, token_overlap_grounding  # Import lightweight helpers under test.


def test_normalize_text_removes_punctuation() -> None:
    """Text normalizer should lowercase and strip punctuation."""

    normalized = normalize_text("Hello, WORLD!!")  # Normalize mixed-case punctuated string.
    assert normalized == "hello world"  # Ensure normalized output is punctuation-free lowercase text.


def test_token_overlap_grounding_scores_supported_answer_higher() -> None:
    """Supported answers should receive higher lexical grounding score."""

    source = "Python was created by Guido van Rossum."  # Define source evidence text.
    grounded = "Guido van Rossum created Python."  # Define grounded answer text.
    hallucinated = "Python was created by Ada Lovelace."  # Define partially unsupported answer text.
    assert token_overlap_grounding(source, grounded) > token_overlap_grounding(source, hallucinated)  # Assert grounded answer receives higher overlap score.
