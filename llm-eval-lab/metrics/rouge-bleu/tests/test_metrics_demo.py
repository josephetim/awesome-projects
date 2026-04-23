"""Tests for ROUGE/BLEU helper functions."""

from src.metrics_demo import compute_bleu, compute_rouge  # Import helper functions under test.


def test_compute_rouge_returns_expected_keys() -> None:
    """ROUGE helper should return standard metric keys."""

    scores = compute_rouge("the cat sat on the mat", "the cat sat on mat")  # Compute ROUGE on similar strings.
    assert set(scores.keys()) == {"rouge1", "rouge2", "rougeL"}  # Ensure all expected ROUGE metrics are present.


def test_compute_bleu_increases_for_better_match() -> None:
    """BLEU should be higher for closer lexical matches."""

    reference = "machine learning improves with more data"  # Define reference sentence.
    close = "machine learning improves with data"  # Define close candidate sentence.
    far = "the weather is sunny today"  # Define unrelated candidate sentence.
    assert compute_bleu(reference, close) > compute_bleu(reference, far)  # Ensure BLEU reflects relative overlap quality.
