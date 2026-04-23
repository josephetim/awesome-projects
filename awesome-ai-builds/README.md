# 🤖 awesome-ai-builds

[![Build Status](https://img.shields.io/github/actions/workflow/status/josephetim/awesome-ai-builds/ci.yml?branch=main&style=flat-square&logo=github)](https://github.com/josephetim/awesome-ai-builds/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](./LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange?style=flat-square&logo=google)](https://aistudio.google.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](./CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/josephetim/awesome-ai-builds?style=flat-square&color=yellow)](https://github.com/josephetim/awesome-ai-builds/stargazers)
[![Contributors](https://img.shields.io/github/contributors/josephetim/awesome-ai-builds?style=flat-square)](https://github.com/josephetim/awesome-ai-builds/graphs/contributors)

> A haven for anyone who wants to pick up an AI project and actually ship it.

Real projects. Real code. Documented well enough that a beginner can follow along,
and extensible enough that an intermediate can make it their own.

---

## ⚡ 30-Second Demo

> **pdf-qa-chatbot** — upload any PDF, ask it anything, get answers grounded in the document.

![pdf-qa-chatbot demo](./assets/demos/pdf-qa-chatbot.gif)

> *The GIF above shows: uploading a 40-page research paper → asking "What are the key findings?" → getting a cited, grounded answer in under 3 seconds.*

```bash
# Three commands. That's all it takes.
git clone https://github.com/your-org/awesome-ai-builds.git
cd awesome-ai-builds/beginner/pdf-qa-chatbot
pip install -r requirements.txt
cp .env.example .env        # paste your free Gemini key (see below)
python app.py               # opens in your browser at localhost:7860
```

> 🔑 **Free to run.** Get your Gemini API key at
> [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
> — sign in with any Gmail account. No credit card. Takes 2 minutes.

---

## 📁 Structure

```
awesome-ai-builds/
├── beginner/                    # Single-file, minimal setup, < 5 commands to run
│   ├── pdf-qa-chatbot/
│   ├── sentiment-classifier/
│   └── email-subject-generator/
├── intermediate/                # Multi-module, real data, some infrastructure
│   ├── ai-research-assistant/
│   ├── image-caption-api/
│   └── code-reviewer-bot/
├── advanced/                    # Production-grade, complex orchestration
│   └── multi-agent-news-analyst/
├── templates/                   # Scaffold for new project contributions
└── resources/                   # Curated courses, papers, tools per category
```

---

## 🗂️ Project Index

| Project | Level | Stack | What It Does |
|---|---|---|---|
| [pdf-qa-chatbot](./beginner/pdf-qa-chatbot) | 🟢 Beginner | LangChain · FAISS · Gradio | Ask questions about any PDF |
| [sentiment-classifier](./beginner/sentiment-classifier) | 🟢 Beginner | HuggingFace · Gradio | Classify text — positive / negative / neutral |
| [email-subject-generator](./beginner/email-subject-generator) | 🟢 Beginner | Gemini · Streamlit | Generate 5 subject lines from an email body |
| [ai-research-assistant](./intermediate/ai-research-assistant) | 🟡 Intermediate | LangGraph · Tavily · Streamlit | Agent that searches the web and synthesizes findings |
| [image-caption-api](./intermediate/image-caption-api) | 🟡 Intermediate | BLIP-2 · FastAPI | REST API that captions any uploaded image |
| [code-reviewer-bot](./intermediate/code-reviewer-bot) | 🟡 Intermediate | FastAPI · PyGithub · Gemini | GitHub bot that reviews pull requests automatically |
| [multi-agent-news-analyst](./advanced/multi-agent-news-analyst) | 🔴 Advanced | CrewAI · PostgreSQL · Celery | 3-agent crew that produces a daily news briefing |

---

## 🚀 Projects In Detail

### 🟢 Beginner

#### 1. PDF Q&A Chatbot
Upload any PDF. Ask questions. Get answers grounded in the document — no
hallucination, no guessing.

**What you'll learn:** Chunking, embeddings, vector search, retrieval, prompt construction  
**Stack:** Python · LangChain · FAISS · Gemini 1.5 Flash · Gradio  
**Time to get running:** ~15 minutes  
→ [`/beginner/pdf-qa-chatbot`](./beginner/pdf-qa-chatbot)

---

#### 2. Sentiment Classifier
Paste any text. Get: positive / negative / neutral + a confidence score.
Runs a local model — no API key needed at all.

**What you'll learn:** HuggingFace inference pipelines, local model inference  
**Stack:** Python · HuggingFace Transformers · Gradio  
**Time to get running:** ~10 minutes  
→ [`/beginner/sentiment-classifier`](./beginner/sentiment-classifier)

---

#### 3. Email Subject Line Generator
Paste an email body. Get 5 subject line options in seconds.

**What you'll learn:** Few-shot prompting, structured output parsing  
**Stack:** Python · Gemini · Streamlit  
**Time to get running:** ~10 minutes  
→ [`/beginner/email-subject-generator`](./beginner/email-subject-generator)

---

### 🟡 Intermediate

#### 4. AI Research Assistant
Enter a research question. An agent searches the web, reads the top results,
and returns a structured summary with cited sources.

**What you'll learn:** LangGraph agent loop, tool calling, state management  
**Stack:** Python · LangGraph · Tavily API (free tier) · Gemini · Streamlit  
→ [`/intermediate/ai-research-assistant`](./intermediate/ai-research-assistant)

---

#### 5. Image Caption API
A REST API that accepts an image upload and returns a natural-language caption.
Runs entirely locally — no API key needed.

**What you'll learn:** Vision-language models, FastAPI, async file handling  
**Stack:** Python · BLIP-2 · FastAPI · Uvicorn  
**Note:** Needs ~6GB RAM minimum. Slow on CPU — GPU recommended.  
→ [`/intermediate/image-caption-api`](./intermediate/image-caption-api)

---

#### 6. Code Reviewer Bot
A GitHub webhook that fires on every pull request, reads the diff,
and posts a structured review comment — automatically.

**What you'll learn:** Webhooks, diff parsing, structured prompting for code review  
**Stack:** Python · FastAPI · PyGithub · Gemini  
→ [`/intermediate/code-reviewer-bot`](./intermediate/code-reviewer-bot)

---

### 🔴 Advanced

#### 7. Multi-Agent News Analyst
Three agents — Researcher, Analyst, Writer — that monitor a topic daily,
identify trends, and produce a formatted briefing stored in PostgreSQL.

**What you'll learn:** CrewAI agent roles, memory, task orchestration, background scheduling  
**Stack:** Python · CrewAI · Serper API · Gemini · PostgreSQL · Celery  
→ [`/advanced/multi-agent-news-analyst`](./advanced/multi-agent-news-analyst)

---

## 📖 What Every Project Includes

```
project-name/
├── README.md           ← plain-English explanation: what, why, how to run
├── architecture.md     ← how it works under the hood (with Mermaid diagram)
├── .env.example        ← every required env var, with setup instructions
├── requirements.txt    ← pinned dependencies
├── llm.py              ← provider adapter: gemini (default) or openai
├── src/                ← annotated source code with inline comments
├── tests/              ← at least one working test
├── EXTEND.md           ← 5 ideas for how to build on this project
└── TROUBLESHOOT.md     ← top 5 errors beginners hit and exactly how to fix them
```

---

## ⚡ AI Provider Setup

Every project runs on **Google Gemini by default — free, no credit card needed.**

```bash
# .env (copy from .env.example and fill in your key)

# FREE ✅ — Default
PROVIDER=gemini
GEMINI_API_KEY=your_key_here     # → https://aistudio.google.com/app/apikey

# PAID 💳 — Optional upgrade
# PROVIDER=openai
# OPENAI_API_KEY=your_key_here
```

The `llm.py` file in every project handles provider switching.
The rest of the codebase never changes — just update your `.env`.

---

## 🤝 Contributing

All levels welcome.

- **New project** → use the [project template](./templates/new-project-template)
- **Improve docs** → fix anything confusing, add examples, add diagrams
- **Good First Issues** → labeled and kept fresh every week

Read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before opening a PR.

**Rule for new projects:** Must run end-to-end with Gemini and a free API key.
No credit card required to contribute or to use.

---

## 📚 Resources

[`/resources`](./resources) contains:
- Learning paths per category (NLP, CV, Agents, RAG)
- Best free courses, ranked and reviewed
- Essential papers with plain-English summaries
- Tool and library comparison guides

---

## 📬 Community

- 💬 Discord: [Join here](#)
- 📅 Monthly build-along: Announced in Discord
- 🐦 Updates: [@awesome_ai_builds](#)

---

## License

MIT — use it, fork it, build on it.
