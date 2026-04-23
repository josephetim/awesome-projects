"""Tests for prompt and parsing logic."""

from src.generator import build_prompt, parse_subjects  # Import helper functions under test.


def test_build_prompt_contains_schema_instruction() -> None:
    """Prompt should enforce strict JSON schema for parser reliability."""

    prompt = build_prompt("Please review the onboarding deck before Friday.")  # Build prompt from sample email body.
    assert "\"subjects\"" in prompt  # Ensure schema key appears in instructions.
    assert "exactly five" in prompt.lower()  # Ensure quantity constraint is explicit.


def test_parse_subjects_from_bulleted_text() -> None:
    """Fallback parser should handle non-JSON bullet lists."""

    raw = "- Kickoff Prep for Monday\n- Monday Kickoff: Read This First\n- Agenda for Monday Kickoff\n- Team Kickoff Checklist\n- Monday Kickoff Reminder"  # Create bullet output shape that models often return.
    subjects = parse_subjects(raw)  # Parse text into standardized output list.
    assert len(subjects) == 5  # Ensure parser always returns exactly five items.
    assert subjects[0].startswith("Kickoff")  # Ensure parser preserves meaningful subject text.
