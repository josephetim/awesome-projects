"""Tests for multi-agent news pipeline utilities."""

from src.news_pipeline import run_multi_agent_pipeline  # Import function under test.


def test_run_multi_agent_pipeline_with_mock_generator() -> None:
    """Pipeline should produce non-empty role outputs with injected generator."""

    sources = [  # Build deterministic source list input for test.
        {"title": "AI Update", "link": "https://example.com/ai", "snippet": "New chip roadmap announced."}
    ]

    def fake_generate(**kwargs: str) -> str:  # Define deterministic fake generator to avoid network/provider dependencies.
        prompt = kwargs.get("prompt", "")  # Read prompt text to branch output by role hints.
        if "Extract key verified facts" in prompt:  # Detect researcher prompt branch.
            return "- Fact: New chip roadmap announced (https://example.com/ai)"  # Return deterministic researcher output.
        if "Analyze trends" in prompt:  # Detect analyst prompt branch.
            return "- Trend: Hardware acceleration focus is increasing."  # Return deterministic analyst output.
        return "## Executive Summary\nChip acceleration focus is rising.\n\n## Sources\n- https://example.com/ai"  # Return deterministic final briefing text.

    outputs = run_multi_agent_pipeline(topic="AI chip market", sources=sources, generate_fn=fake_generate)  # Execute pipeline with injected generator.
    assert "Fact:" in outputs.researcher_notes  # Ensure researcher output is populated.
    assert "Trend:" in outputs.analyst_notes  # Ensure analyst output is populated.
    assert "Executive Summary" in outputs.briefing  # Ensure writer briefing output is populated.
