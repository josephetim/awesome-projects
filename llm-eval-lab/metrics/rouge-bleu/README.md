# ROUGE and BLEU Explorer

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/builders-triad/llm-eval-lab/blob/main/metrics/rouge-bleu/rouge_bleu_explainer.ipynb)

`rouge-bleu` is an interactive notebook module that explains, computes, and critiques ROUGE and BLEU.

## Why This Exists

Teams often misread overlap metrics as complete quality scores.  
This module teaches what ROUGE/BLEU measure, what they miss, and how to interpret scores safely.

## Skill Level

`beginner`

## Stack

- Python
- rouge-score
- nltk
- Jupyter notebook

## What It Teaches

- when to use ROUGE vs BLEU
- what each metric emphasizes (recall vs precision tendencies)
- where both metrics fail (paraphrases, factuality, style quality)
- common misinterpretations in benchmark reporting

## Run

1. `cd metrics/rouge-bleu`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `jupyter notebook rouge_bleu_explainer.ipynb`

## Run Tests

- `pytest tests/ -q`
