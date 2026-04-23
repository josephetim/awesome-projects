# Annotation Tool

`annotation-tool` is a lightweight web app for human evaluation of LLM outputs on relevance, accuracy, and tone.

## Why This Exists

Automated metrics miss many nuanced quality issues.  
This module demonstrates when and how to use structured human annotation with agreement analysis.

## Skill Level

`intermediate`

## Stack

- Python
- FastAPI
- SQLite
- Jinja2

## Input and Output

- Input:
  - human ratings for each item on relevance, accuracy, tone
- Output:
  - stored annotation records
  - agreement stats including Fleiss’ Kappa

## No External Model APIs

- This project does not require `llm.py`.
- No model API key is needed.

## Run

1. `cd human-eval/annotation-tool`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`
6. Open `http://127.0.0.1:8000`

## Rubric Design Notes

- Relevance: does the response address the prompt?
- Accuracy: is content factually correct and non-misleading?
- Tone: is language appropriate and professional for the context?

## Run Tests

- `pytest tests/ -q`
