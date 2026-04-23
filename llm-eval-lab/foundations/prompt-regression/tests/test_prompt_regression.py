"""Pytest-based prompt regression suite driven by YAML cases."""

from __future__ import annotations

from pathlib import Path  # Import Path to resolve local YAML case file path.

import pytest  # Import pytest for parametrized test execution.

from src.prompt_regression import evaluate_case, load_cases  # Import case loader and evaluator utilities.

CASE_FILE = Path(__file__).with_name("cases.yaml")  # Resolve YAML test case file colocated with this test module.
CASES = load_cases(CASE_FILE)  # Load all cases once for pytest parameterization.


def fake_generator(prompt: str, **_: str) -> str:
    """Deterministic model stub for offline test execution."""

    if "capital of france" in prompt.lower():  # Detect exact-match case prompt.
        return "Paris"  # Return expected exact answer.
    if "safe coding practices" in prompt.lower():  # Detect contains-match case prompt.
        return "Use input validation and apply least privilege in access control."  # Return string containing required keywords.
    if "you are an evaluation judge" in prompt.lower():  # Detect judge evaluator prompt.
        return "PASS"  # Return passing judge verdict for harmful request refusal case.
    return "I cannot help with illegal harm."  # Return safe refusal fallback for harmful prompt.


@pytest.mark.parametrize("case", CASES, ids=[case.case_id for case in CASES])
def test_prompt_case(case) -> None:
    """Each YAML case should pass according to its configured strategy."""

    passed, reason, actual = evaluate_case(case, generate_fn=fake_generator)  # Evaluate one case using deterministic stub generator.
    assert passed, f"Case '{case.case_id}' failed: {reason}. Actual output: {actual}"  # Emit explicit failure details when case does not pass.
