# RAGAS Pipeline

`ragas-pipeline` builds a small RAG app and evaluates it with RAGAS-style metrics: faithfulness, context recall, and answer relevance.

## Why This Exists

Many RAG demos stop at retrieval and answer generation.  
This module shows how to measure RAG quality and interpret weak metric outcomes.

## Skill Level

`intermediate`

## Stack

- Python
- RAGAS
- FAISS
- Streamlit
- project-level `llm.py`

## Input and Output

- Input: user question
- Output:
  - retrieved context chunks
  - generated answer
  - evaluation metrics (faithfulness, context recall, answer relevance)

## Provider Setup

- Default free path: `PROVIDER=gemini`
- Optional paid path: `PROVIDER=openai`

## Run

1. `cd frameworks/ragas-pipeline`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Add API key values
7. `python app.py`

## Metric Interpretation

- Low faithfulness: answer likely introduces unsupported claims.
- Low context recall: retrieval is missing relevant evidence.
- Low answer relevance: answer may be off-topic or too generic.

## Improving Weak Scores

- Tune chunk size and overlap.
- Improve retrieval query expansion.
- Add better source documents.
- Add stricter answer grounding instructions.

## Run Tests

- `pytest tests/ -q`
