# Hallucination Detection

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/builders-triad/llm-eval-lab/blob/main/metrics/hallucination-detection/hallucination_detection.ipynb)

`hallucination-detection` scores how grounded a generated answer is relative to source text.

## Why This Exists

Fluent answers can still be incorrect.  
This module demonstrates local grounding signals that help detect unsupported generation.

## Skill Level

`intermediate`

## Stack

- Python
- BERTScore
- sentence-transformers
- Jupyter notebook

## Input and Output

- Input:
  - source text
  - generated answer
- Output:
  - lexical overlap score
  - semantic similarity score
  - BERTScore F1
  - combined grounding score

## Local-Only Rule

- No external LLM APIs are used.
- No `llm.py` is required.

## Run

1. `cd metrics/hallucination-detection`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `jupyter notebook hallucination_detection.ipynb`

## Example Dataset

- `data/example_dataset.csv` contains grounded and weakly grounded examples for experimentation.

## Run Tests

- `pytest tests/ -q`

## Limitations

- Similarity metrics can over-score confident paraphrases that still contain factual errors.
- Grounding checks depend heavily on source text coverage and quality.
