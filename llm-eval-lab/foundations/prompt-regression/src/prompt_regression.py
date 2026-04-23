"""YAML-driven prompt regression evaluation utilities."""

from __future__ import annotations

from dataclasses import dataclass  # Import dataclass for structured test case definitions.
from pathlib import Path  # Import Path for filesystem-safe YAML loading.
from typing import Callable  # Import Callable to support dependency injection in tests.

import yaml  # Import PyYAML for loading prompt test case definitions.

from llm import generate_text  # Import local provider adapter for model generation and judge scoring.


@dataclass
class PromptCase:
    """Structured prompt test case."""

    case_id: str  # Unique identifier used for pytest test IDs and logs.
    prompt: str  # Prompt text to send to model.
    strategy: str  # Evaluation strategy name: exact, contains, or judge.
    expected: str | list[str]  # Expected answer string or required token list.
    judge_rubric: str | None = None  # Optional rubric used only by judge strategy.


def load_cases(path: str | Path) -> list[PromptCase]:
    """Load prompt regression cases from YAML file."""

    file_path = Path(path)  # Normalize path input to pathlib object.
    data = yaml.safe_load(file_path.read_text(encoding="utf-8"))  # Parse YAML content into Python dictionary.
    cases_data = data.get("cases", []) if isinstance(data, dict) else []  # Extract top-level cases array safely.
    cases: list[PromptCase] = []  # Initialize output list for parsed prompt cases.
    for item in cases_data:  # Iterate through each YAML case entry.
        case = PromptCase(  # Build typed case object from YAML values.
            case_id=str(item["id"]).strip(),  # Read and normalize case identifier.
            prompt=str(item["prompt"]).strip(),  # Read and normalize prompt text.
            strategy=str(item["strategy"]).strip().lower(),  # Normalize evaluation strategy label.
            expected=item["expected"],  # Keep expected data type as string or list for strategy-specific checks.
            judge_rubric=str(item.get("judge_rubric", "")).strip() or None,  # Normalize optional judge rubric field.
        )
        cases.append(case)  # Append parsed case to output list.
    return cases  # Return all parsed cases for parameterized tests.


def _normalize(text: str) -> str:
    """Normalize text for string-based comparisons."""

    return " ".join(text.strip().lower().split())  # Lowercase and collapse whitespace for robust comparisons.


def evaluate_exact(expected: str, actual: str) -> tuple[bool, str]:
    """Evaluate exact normalized equality."""

    passed = _normalize(expected) == _normalize(actual)  # Compare normalized expected and actual strings.
    reason = "exact_match" if passed else f"expected='{expected}' actual='{actual}'"  # Build detailed reason message for reporting.
    return passed, reason  # Return pass flag and reason text.


def evaluate_contains(expected: str | list[str], actual: str) -> tuple[bool, str]:
    """Evaluate whether required substring(s) exist in output."""

    required = [expected] if isinstance(expected, str) else list(expected)  # Normalize expected values into list form.
    actual_norm = _normalize(actual)  # Normalize model output for case-insensitive containment checks.
    missing: list[str] = []  # Track missing required tokens for failure diagnostics.
    for token in required:  # Iterate over each required token.
        token_norm = _normalize(str(token))  # Normalize required token text.
        if token_norm not in actual_norm:  # Check whether required token appears in normalized output.
            missing.append(str(token))  # Record missing token for failure explanation.
    passed = not missing  # Pass only when all required tokens are present.
    reason = "contains_match" if passed else f"missing_tokens={missing}"  # Build detailed reason output.
    return passed, reason  # Return pass state and reason string.


def _judge_prompt(case: PromptCase, actual: str) -> str:
    """Build LLM-as-judge prompt."""

    rubric = case.judge_rubric or "Assess whether the answer addresses the prompt accurately and safely."  # Use case rubric when provided, else fallback rubric.
    return (  # Build strict judge prompt requiring PASS/FAIL output.
        "You are an evaluation judge.\n"  # Define evaluator role.
        "Return exactly one word: PASS or FAIL.\n"  # Enforce parseable single-token output.
        f"Rubric: {rubric}\n\n"  # Provide grading rubric.
        f"Prompt: {case.prompt}\n"  # Provide original prompt context.
        f"Expected: {case.expected}\n"  # Provide expected behavior description.
        f"Actual: {actual}\n"  # Provide model output under evaluation.
    )


def evaluate_case(case: PromptCase, generate_fn: Callable[..., str] | None = None) -> tuple[bool, str, str]:
    """Run one prompt case and return pass/fail details."""

    generator = generate_fn or generate_text  # Resolve generation function with test injection support.
    actual = generator(prompt=case.prompt, system_prompt="You are a precise assistant.", temperature=0.0, max_tokens=350)  # Generate output for current prompt case.

    if case.strategy == "exact":  # Run exact evaluator branch.
        passed, reason = evaluate_exact(str(case.expected), actual)  # Evaluate strict normalized equality.
    elif case.strategy == "contains":  # Run contains evaluator branch.
        passed, reason = evaluate_contains(case.expected, actual)  # Evaluate required token inclusion.
    elif case.strategy == "judge":  # Run LLM-as-judge evaluator branch.
        judge_output = generator(  # Generate PASS/FAIL verdict from evaluator prompt.
            prompt=_judge_prompt(case, actual),  # Send judge prompt with rubric and outputs.
            system_prompt="You are a strict grading assistant.",  # Set strict evaluator behavior.
            temperature=0.0,  # Keep judge deterministic.
            max_tokens=10,  # Limit judge output to short verdict.
        )
        verdict = judge_output.strip().upper()  # Normalize judge output for robust PASS/FAIL parsing.
        passed = verdict.startswith("PASS")  # Treat outputs beginning with PASS as pass verdict.
        reason = f"judge_verdict={verdict}"  # Return raw verdict for transparent diagnostics.
    else:  # Handle unsupported strategy values.
        raise ValueError(f"Unsupported strategy: {case.strategy}")  # Raise explicit error for invalid strategy.

    return passed, reason, actual  # Return evaluation outcome and generated output for pytest assertions.
