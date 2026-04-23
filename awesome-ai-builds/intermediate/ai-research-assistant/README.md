# AI Research Assistant

`ai-research-assistant` takes a research question, searches the web, and generates a structured summary with source citations.

## Why This Exists

Developers need practical examples of tool-augmented agents with clear state handling.  
This project demonstrates search tool usage, state transitions, and result synthesis in one workflow.

## Skill Level

`intermediate`

## Stack

- Python
- LangGraph
- Tavily Search API
- Streamlit
- local provider adapter (`llm.py`)

## Input and Output

- Input: one research question
- Output:
  - structured summary
  - cited source list with links

## Provider Setup

- Default free path: `PROVIDER=gemini`
- Optional paid path: `PROVIDER=openai`

## Tavily Setup (Free Tier Available)

1. Create an account at https://tavily.com/
2. Generate an API key in your dashboard.
3. Put it in `.env` as `TAVILY_API_KEY=...`

Tavily offers a free tier suitable for learning and small experiments.

## Run Locally

1. `cd intermediate/ai-research-assistant`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Add `GEMINI_API_KEY` (or OpenAI key) and `TAVILY_API_KEY`
7. `python app.py`

## Run Tests

- `pytest tests/ -q`

## Concepts Taught

- agent loop structure
- tool calling with search
- state management with graph nodes
- synthesis and citation formatting
