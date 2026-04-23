# Prompt Regression

`prompt-regression` provides YAML-driven prompt tests that run in `pytest`.

## Why This Exists

Prompt changes and model upgrades often cause silent behavior drift.  
This module helps teams catch regressions by encoding expected behavior as test cases.

## Skill Level

`beginner`

## Stack

- Python
- pytest
- PyYAML
- project-level `llm.py`

## Evaluation Strategies Included

- `exact`: strict string equality after normalization
- `contains`: checks required substring(s)
- `judge`: uses LLM-as-judge for rubric-based grading

## Input and Output

- Input: YAML test cases
- Output: pytest pass/fail with clear failure reasons and model outputs

## Provider Setup

- Default free path: `PROVIDER=gemini`
- Optional paid path: `PROVIDER=openai`

## Run

1. `cd foundations/prompt-regression`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Add API key values
7. `pytest tests/ -q`
