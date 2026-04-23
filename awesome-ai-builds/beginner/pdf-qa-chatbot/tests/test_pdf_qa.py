"""Unit tests for PDF QA prompt utilities."""

from src.pdf_qa import build_prompt, format_context  # Import pure helper functions for lightweight test coverage.


def test_format_context_numbers_chunks() -> None:
    """Context formatter should include stable numbered chunk labels."""

    rendered = format_context(["Chunk one content", "Chunk two content"])  # Build formatted context from two sample chunks.
    assert "[Chunk 1] Chunk one content" in rendered  # Verify first chunk label and content are present.
    assert "[Chunk 2] Chunk two content" in rendered  # Verify second chunk label and content are present.


def test_build_prompt_includes_question_and_context() -> None:
    """Prompt builder should include both the question and retrieved evidence."""

    prompt = build_prompt("What is the conclusion?", ["The report concludes that latency improved by 34%."])  # Build prompt with one evidence chunk.
    assert "What is the conclusion?" in prompt  # Ensure question text is retained inside final prompt.
    assert "latency improved by 34%" in prompt  # Ensure retrieved evidence is embedded into prompt context.
