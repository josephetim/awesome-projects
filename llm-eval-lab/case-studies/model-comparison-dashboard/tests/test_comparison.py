"""Tests for comparison scoring and aggregation helpers."""

import pandas as pd  # Import pandas for test DataFrame construction.

from src.comparison import aggregate_scores, score_output  # Import functions under test.


def test_score_output_returns_expected_keys() -> None:
    """Score function should return complete rubric fields."""

    scores = score_output("Explain binary search", "Binary search finds an item in a sorted list by halving the search range each step.")  # Score sample prompt/output pair.
    assert set(scores.keys()) == {"relevance", "clarity", "safety", "completeness", "overall"}  # Validate complete metric key set.


def test_aggregate_scores_groups_by_provider() -> None:
    """Aggregator should compute provider-level means."""

    frame = pd.DataFrame(  # Build synthetic benchmark rows for aggregation test.
        [
            {"provider": "gemini", "relevance": 0.9, "clarity": 0.8, "safety": 1.0, "completeness": 0.7, "overall": 0.86},
            {"provider": "gemini", "relevance": 0.8, "clarity": 0.8, "safety": 1.0, "completeness": 0.6, "overall": 0.8},
            {"provider": "openai", "relevance": 0.7, "clarity": 0.9, "safety": 1.0, "completeness": 0.8, "overall": 0.83},
        ]
    )
    agg = aggregate_scores(frame)  # Aggregate synthetic results by provider.
    assert set(agg["provider"]) == {"gemini", "openai"}  # Ensure both providers appear in output.
    gemini_overall = float(agg.loc[agg["provider"] == "gemini", "overall"].iloc[0])  # Extract Gemini aggregated overall score.
    assert 0.8 <= gemini_overall <= 0.86  # Validate Gemini mean falls in expected range.
