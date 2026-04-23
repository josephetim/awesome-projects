# llm-eval-lab

`llm-eval-lab` is a practical repository for evaluating LLM quality with automated metrics, framework-based pipelines, case studies, and human annotation workflows.

## Why Evaluation Matters

Without evaluation, prompt and model improvements are guesswork.  
This lab helps teams measure reliability, groundedness, bias, and consistency before shipping AI features.

## Metrics Quick Reference

| Metric / Method | Measures | Best For | Main Limitation |
|---|---|---|---|
| Exact Match | strict string equality | deterministic outputs | too brittle for paraphrases |
| Contains Match | key phrase presence | keyword-oriented checks | ignores nuance and correctness depth |
| LLM-as-Judge | rubric-based semantic quality | open-ended generation | evaluator model bias |
| BERTScore | semantic similarity | abstractive outputs | can reward fluent hallucinations |
| ROUGE | n-gram overlap recall/precision | summarization | misses semantic equivalence |
| BLEU | n-gram precision | translation-style tasks | harsh on valid paraphrases |
| RAGAS Faithfulness | claim grounding in context | RAG systems | sensitive to context quality |

## Module Index

| Area | Module | Skill Level | Stack | Description |
|---|---|---|---|---|
| foundations | `prompt-regression` | beginner | Python, pytest, YAML, `llm.py` | YAML-driven prompt tests with exact/contains/judge evaluators. |
| metrics | `hallucination-detection` | intermediate | Python, BERTScore, sentence-transformers, notebook | Scores how grounded answers are against source text. |
| metrics | `rouge-bleu` | beginner | Python, rouge-score, nltk, notebook | Interactive explainer for ROUGE/BLEU strengths and weaknesses. |
| frameworks | `ragas-pipeline` | intermediate | Python, RAGAS, FAISS, Streamlit, `llm.py` | Mini RAG system with quality scoring and interpretation guidance. |
| case-studies | `model-comparison-dashboard` | intermediate | Python, Streamlit, Plotly, `llm.py` | Side-by-side provider benchmarking dashboard. |
| case-studies | `bias-audit` | intermediate | Python, Pandas, Plotly, Streamlit, `llm.py` | Counterfactual bias auditing with disparity visualizations. |
| human-eval | `annotation-tool` | intermediate | Python, FastAPI, SQLite, Jinja2 | Human rating interface with inter-annotator agreement. |

## Shared Provider Rule

For modules using external LLM APIs:

- provider logic is isolated in local `llm.py`
- supported providers are exactly `gemini` and `openai`
- default provider is always `gemini`

## Repository Layout

```text
llm-eval-lab/
├── README.md
├── CONTRIBUTING.md
├── llm.py
├── foundations/
├── metrics/
├── frameworks/
├── case-studies/
└── human-eval/
```
