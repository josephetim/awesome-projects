# awesome-ai-builds

<p align="left">
  <img src="https://img.shields.io/github/license/josephetim/awesome-projects?color=blue" />
  <img src="https://img.shields.io/github/stars/josephetim/awesome-projects?style=social" />
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
  <img src="https://img.shields.io/badge/AI-Gemini%20%7C%20OpenAI-blueviolet" />
  <img src="https://img.shields.io/badge/Framework-LangChain%20%7C%20CrewAI-orange" />
</p>


> **No fluff. No toy tutorials.** Real AI projects documented for humans, ranging from single-file scripts to multi-agent production pipelines.

`awesome-ai-builds` is a production-ready collection of end-to-end AI projects across beginner, intermediate, and advanced levels.


> **No fluff. No toy tutorials.** Real AI projects documented for humans, ranging from single-file scripts to multi-agent production pipelines.

## Why This Repository Exists

Many AI project lists stop at demos that are hard to run, hard to extend, or unclear for beginners.  
This repository focuses on practical builds with clean architecture, tests, clear setup instructions, and explicit extension guidance.

## Shared Provider Rule

Every project that calls an LLM isolates provider logic in a project-root `llm.py`.

- Default provider: `gemini` (free path)
- Optional provider: `openai` (paid upgrade)
- Provider selection: `PROVIDER=` in `.env`
- If `PROVIDER` is missing, projects default to `gemini`

## Project Index

| Level | Project | Entry Point | Stack | One-Line Description |
|---|---|---|---|---|
| beginner | `pdf-qa-chatbot` | `python app.py` | Python, LangChain, FAISS, Gradio | Ask questions against uploaded PDFs using retrieval-augmented generation. |
| beginner | `sentiment-classifier` | `python app.py` | Python, Transformers, Gradio | Local sentiment classification with confidence scores and no API key. |
| beginner | `email-subject-generator` | `python app.py` | Python, Streamlit, LLM adapter | Generates five subject lines from an email body using few-shot prompting. |
| intermediate | `ai-research-assistant` | `python app.py` | Python, LangGraph, Tavily, Streamlit | Runs a tool-augmented research loop and outputs structured summaries with sources. |
| intermediate | `image-caption-api` | `uvicorn main:app --reload` | Python, FastAPI, BLIP-2, Uvicorn | REST API that captions uploaded images using a local vision-language model. |
| intermediate | `code-reviewer-bot` | `uvicorn main:app --reload` | Python, FastAPI, PyGithub, LLM adapter | GitHub webhook bot that reviews PR diffs and posts structured comments. |
| advanced | `multi-agent-news-analyst` | `python main.py --topic "..."` | Python, CrewAI, Serper, PostgreSQL, Celery, Redis | Three-agent pipeline that collects, analyzes, and writes daily news briefings. |

## Quick Start

1. Clone this repository.
2. Pick any project folder.
3. Copy `.env.example` to `.env`.
4. Keep `PROVIDER=gemini` for the free default in LLM-based projects.
5. Install dependencies with `pip install -r requirements.txt`.
6. Run the project using the entry point in its README.

## Repository Layout

```text
awesome-ai-builds/
├── README.md
├── CONTRIBUTING.md
├── llm.py
├── templates/new-project-template/
├── resources/README.md
├── beginner/
├── intermediate/
└── advanced/
```

## Third-Party Keys

- Gemini API key: optional free-tier path for LLM projects.
- OpenAI API key: optional paid path for LLM projects.
- Tavily API key: required only for `ai-research-assistant` (free tier available).
- Serper API key: required only for `multi-agent-news-analyst` (free tier available).

Every project README includes exact key setup details.
