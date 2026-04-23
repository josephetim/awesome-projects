"""Tests for research workflow helpers."""

from src.research_assistant import build_synthesis_prompt, run_research  # Import functions under test.


def test_build_synthesis_prompt_contains_evidence() -> None:
    """Prompt should contain question and source evidence text."""

    prompt = build_synthesis_prompt(  # Build synthesis prompt from deterministic sample data.
        "What is synthetic data?",
        [{"title": "Synthetic Data Overview", "url": "https://example.com", "content": "Synthetic data is generated data used for model training."}],
    )
    assert "What is synthetic data?" in prompt  # Ensure question is embedded in prompt.
    assert "https://example.com" in prompt  # Ensure URL evidence appears for citation grounding.


def test_run_research_with_injected_dependencies() -> None:
    """Workflow should run end-to-end with mock search and generation functions."""

    def fake_search(question: str) -> list[dict]:  # Define deterministic fake search function for isolated testing.
        return [{"title": "Result", "url": "https://source.test", "content": f"Evidence for {question}"}]  # Return one deterministic search result.

    def fake_generate(**_: str) -> str:  # Define deterministic fake generation function to avoid API calls in tests.
        return "## Executive Summary\nMock summary\n\n## Sources\n- https://source.test"  # Return predictable markdown summary.

    state = run_research("test question", search_fn=fake_search, generate_fn=fake_generate)  # Execute workflow with injected dependencies.
    assert state["summary"].startswith("## Executive Summary")  # Ensure summary field is populated from fake generation output.
    assert state["sources"] == ["https://source.test"]  # Ensure source extraction logic preserved URL from fake search results.
