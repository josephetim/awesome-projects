# Bias Audit

`bias-audit` runs counterfactual prompt pairs to surface potential demographic and occupational response disparities.

## Why This Exists

Bias can appear even when answers look fluent and helpful.  
This module helps teams systematically probe differences across equivalent prompt variants.

## Skill Level

`intermediate`

## Stack

- Python
- Pandas
- Plotly
- Streamlit
- project-level `llm.py`

## Input and Output

- Input:
  - counterfactual prompt pairs (`data/prompt_pairs.csv`)
- Output:
  - pair-level disparities
  - grouped disparity charts
  - summary table for audit reporting

## Provider Setup

- Default free path: `PROVIDER=gemini`
- Optional paid path: `PROVIDER=openai`

## Concepts Taught

- counterfactual prompting
- disparity score interpretation
- limitations of automated bias heuristics

## Run

1. `cd case-studies/bias-audit`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Add API key values
7. `python app.py`

## Run Tests

- `pytest tests/ -q`
