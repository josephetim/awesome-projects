"""Tests for RAGAS pipeline helper utilities."""

from src.ragas_pipeline import build_prompt, heuristic_rag_scores  # Import lightweight helpers under test.


def test_build_prompt_contains_question_and_context() -> None:
    """Prompt should include both question and context content."""

    prompt = build_prompt("What changed?", ["The release reduced hallucinations by 18 percent."])  # Build prompt with one context chunk.
    assert "What changed?" in prompt  # Ensure question appears in final prompt.
    assert "reduced hallucinations" in prompt  # Ensure context evidence appears in final prompt.


def test_heuristic_scores_return_valid_ranges() -> None:
    """Fallback metrics should remain within [0, 1]."""

    metrics = heuristic_rag_scores(  # Compute heuristic scores for deterministic sample.
        "What is required for incident reports?",
        "Incident reports must be filed within 24 hours.",
        ["Incident reports must be filed within 24 hours for AI safety failures."],
    )
    assert 0.0 <= metrics["faithfulness"] <= 1.0  # Validate faithfulness score range.
    assert 0.0 <= metrics["context_recall"] <= 1.0  # Validate context recall score range.
    assert 0.0 <= metrics["answer_relevance"] <= 1.0  # Validate answer relevance score range.
