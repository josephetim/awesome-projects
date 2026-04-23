# Builder's Triad Ecosystem Index

## Top-Level Deliverables

- [awesome-ai-builds](./awesome-ai-builds)
- [llm-eval-lab](./llm-eval-lab)
- [secure-builder-kit](./secure-builder-kit)
- [repo-hub.html](./repo-hub.html)

## Repository 1: awesome-ai-builds

| Module | Skill Level | Stack | One-Line Description |
|---|---|---|---|
| `beginner/pdf-qa-chatbot` | beginner | Python, LangChain, FAISS, Gradio, `llm.py` | Upload PDF, retrieve relevant chunks, and answer grounded questions. |
| `beginner/sentiment-classifier` | beginner | Python, Transformers, Gradio | Local sentiment classification with confidence and no API key. |
| `beginner/email-subject-generator` | beginner | Python, Streamlit, `llm.py` | Generates five email subject lines using few-shot prompting and parsing. |
| `intermediate/ai-research-assistant` | intermediate | Python, LangGraph, Tavily, Streamlit, `llm.py` | Tool-augmented research loop with structured summary and sources. |
| `intermediate/image-caption-api` | intermediate | Python, FastAPI, BLIP-2 | REST API that captions uploaded images locally. |
| `intermediate/code-reviewer-bot` | intermediate | Python, FastAPI, PyGithub, `llm.py` | GitHub webhook PR reviewer with structured feedback output. |
| `advanced/multi-agent-news-analyst` | advanced | Python, CrewAI, Serper, PostgreSQL, Celery, Redis, `llm.py` | Multi-agent daily news briefing pipeline with background jobs and storage. |

## Repository 2: llm-eval-lab

| Module | Skill Level | Stack | One-Line Description |
|---|---|---|---|
| `foundations/prompt-regression` | beginner | Python, pytest, YAML, `llm.py` | YAML-defined prompt tests with exact/contains/judge evaluators. |
| `metrics/hallucination-detection` | intermediate | Python, BERTScore, sentence-transformers, notebook | Local grounding scoring for source-vs-answer hallucination detection. |
| `metrics/rouge-bleu` | beginner | Python, rouge-score, nltk, notebook | Interactive ROUGE/BLEU explainer with examples and caveats. |
| `frameworks/ragas-pipeline` | intermediate | Python, RAGAS, FAISS, Streamlit, `llm.py` | Mini RAG app with faithfulness/context-recall/answer-relevance scoring. |
| `case-studies/model-comparison-dashboard` | intermediate | Python, Streamlit, Plotly, `llm.py` | Runs prompts across Gemini/OpenAI and visualizes rubric scores. |
| `case-studies/bias-audit` | intermediate | Python, Pandas, Plotly, Streamlit, `llm.py` | Counterfactual prompt-pair bias audit with disparity metrics. |
| `human-eval/annotation-tool` | intermediate | Python, FastAPI, SQLite, Jinja2 | Human annotation UI with rating storage and Fleiss’ Kappa. |

## Repository 3: secure-builder-kit

| Module | Skill Level | Stack | One-Line Description |
|---|---|---|---|
| `lab-setup` | beginner | Docker Compose | Starts local DVWA + Ubuntu lab containers safely. |
| `foundations/networking-basics` | beginner | Python, socket, requests, dnspython, notebook | Observational DNS/TCP/HTTP learning scripts. |
| `web-security/owasp-top-10` | intermediate | Python + DVWA/local labs | OWASP category walkthroughs with safe local demos and defenses. |
| `web-security/sql-injection` | intermediate | Python, requests, BeautifulSoup, DVWA | Deep SQLi lab for basic/UNION/blind boolean/blind time-based techniques. |
| `web-security/jwt-lab` | advanced | Python, FastAPI, python-jose, Docker | Vulnerable JWT app, secure app, and exploit demos for key JWT failures. |
| `network-security/packet-analyzer` | intermediate | Python, Scapy, Rich | Live packet capture and protocol breakdown for authorized interfaces. |
| `tools/port-scanner` | intermediate | Python, socket, threading, argparse, Rich | Fast TCP scanner with CIDR targets, banner grab, and export outputs. |
| `ctf-writeups` | beginner | Markdown | Safe and legal CTF writeup submission guidelines. |
| `resources/certifications` | beginner | Markdown | Certification roadmaps for Security+, CEH, eJPT, and OSCP. |
