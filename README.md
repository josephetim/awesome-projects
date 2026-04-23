

# 🤖 awesome-ai

<p align="left">
  <a href="[https://github.com/josephetim/awesome-ai/blob/main/LICENSE](https://github.com/josephetim/awesome-ai/blob/main/LICENSE)">
    <img src="[https://img.shields.io/github/license/josephetim/awesome-ai?color=blue](https://img.shields.io/github/license/josephetim/awesome-ai?color=blue)" alt="License" />
  </a>
  <a href="[https://github.com/josephetim/awesome-ai/stargazers](https://github.com/josephetim/awesome-ai/stargazers)">
    <img src="[https://img.shields.io/github/stars/josephetim/awesome-ai?style=social](https://img.shields.io/github/stars/josephetim/awesome-ai?style=social)" alt="Stars" />
  </a>
  <img src="[https://img.shields.io/badge/Maintained%3F-yes-green.svg](https://img.shields.io/badge/Maintained%3F-yes-green.svg)" alt="Maintained" />
  <img src="[https://img.shields.io/badge/AI-Gemini%20%7C%20OpenAI-blueviolet](https://img.shields.io/badge/AI-Gemini%20%7C%20OpenAI-blueviolet)" alt="AI Providers" />
</p>

> **No fluff. No toy tutorials.** A curated collection of end-to-end AI projects ranging from single-file scripts to multi-agent production pipelines, documented for humans.

---

## 🚀 Why This Repository Exists

Most AI project lists stop at "Hello World" demos that are hard to run or extend. This repository focuses on **practical builds** with:
- **Clean Architecture:** No "spaghetti code"; logic is modular and tested.
- **Clear Setup:** Explicit `.env` and dependency instructions.
- **Extension Guidance:** Every project includes ideas on how to take it further.

---

## 🛠️ The Shared Provider Rule

To make these projects accessible to everyone, we use a unified LLM adapter pattern located in the root `llm.py`.

- **Default:** `gemini` (The free-tier path).
- **Upgrade:** `openai` (The paid-tier path).
- **Config:** Simply set `PROVIDER=gemini` or `PROVIDER=openai` in your `.env` file.

---

## 🗂️ Project Index

| Level | Project | Stack | Description |
|---|---|---|---|
| 🟢 **Beginner** | `pdf-qa-chatbot` | LangChain, FAISS, Gradio | RAG-based Q&A against uploaded PDFs. |
| 🟢 **Beginner** | `sentiment-classifier` | Transformers, Gradio | Local classification with no API keys required. |
| 🟡 **Intermediate** | `ai-research-assistant` | LangGraph, Tavily | Tool-augmented research loop with structured sources. |
| 🟡 **Intermediate** | `code-reviewer-bot` | FastAPI, PyGithub | Webhook bot that reviews PR diffs and posts comments. |
| 🔴 **Advanced** | `multi-agent-analyst` | CrewAI, PostgreSQL | Three-agent pipeline for daily news briefings. |

---

## 🏃 Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/josephetim/awesome-ai.git
   cd awesome-ai
   ```

2. **Setup environment:**
   ```bash
   cp .env.example .env
   # Add your API keys and set PROVIDER=gemini
   ```

3. **Install and Run:**
   Navigate to any project folder (e.g., `beginner/pdf-qa-chatbot`) and follow the local `README.md`.

---

## 📂 Repository Layout

```text
awesome-ai/
├── beginner/          # Single-file, clear scope, minimal setup
├── intermediate/      # Multi-module, real datasets, some infra
├── advanced/          # Production-grade, complex pipelines
├── llm.py             # Unified LLM provider logic
├── templates/         # Starter kits for new projects
└── resources/         # Curated reading and tool comparisons
```

---

## 🤝 Contributing

We love contributions! Whether it's fixing a typo or adding a whole new project:
1. Check the [Project Template](./templates/new-project-template).
2. Open an issue to discuss your idea.
3. Submit a PR.

Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) for full details.

---

## 📬 Connect & Support

- **LinkedIn:** [josephetim](https://www.linkedin.com/in/josephetim)

*Don't forget to ⭐ this repo if you find it useful!*
