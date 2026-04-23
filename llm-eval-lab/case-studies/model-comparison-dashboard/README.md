# Model Comparison Dashboard

`model-comparison-dashboard` runs the same prompt set against Gemini and OpenAI, scores outputs, and visualizes performance differences.

## Why This Exists

Provider selection decisions should be evidence-driven, not anecdotal.  
This module helps teams benchmark outputs using a repeatable prompt set and rubric.

## Skill Level

`intermediate`

## Stack

- Python
- Streamlit
- Plotly
- Pandas
- project-level `llm.py`

## Input and Output

- Input:
  - prompt dataset (`data/prompts.csv`)
- Output:
  - provider-wise output table
  - rubric scores
  - aggregate comparison charts

## Provider Setup

- Adapter supports exactly two providers: `gemini` and `openai`.
- Default provider remains `gemini`, but this case study can call both providers for side-by-side evaluation.

## Run

1. `cd case-studies/model-comparison-dashboard`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Add both API keys for full comparison
7. `python app.py`

## Benchmark Design Tips

- Include prompts from multiple categories (reasoning, summarization, instruction following, safety).
- Keep prompts stable between runs.
- Track score drift over time as models or prompts change.

## Run Tests

- `pytest tests/ -q`
