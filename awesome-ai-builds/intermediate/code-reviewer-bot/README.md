# Code Reviewer Bot

`code-reviewer-bot` is a GitHub webhook service that reviews pull request diffs and posts structured feedback comments.

## Why This Exists

This project teaches practical webhook integration, diff parsing, and LLM-guided code review automation with explicit review categories.

## Skill Level

`intermediate`

## Stack

- Python
- FastAPI
- PyGithub
- python-dotenv
- project-level `llm.py`

## Input and Output

- Input: GitHub `pull_request` webhook events
- Output: structured review comment on the PR covering:
  - correctness
  - risks
  - readability
  - tests

## Provider Setup

- Free default path: `PROVIDER=gemini`
- Optional paid path: `PROVIDER=openai`

## GitHub Webhook Setup (Step-by-Step)

1. Create a GitHub personal access token with repo comment/write permissions.
2. Clone this project and create `.env` from `.env.example`.
3. Add:
   - `GITHUB_TOKEN`
   - `GITHUB_WEBHOOK_SECRET`
   - LLM provider keys
4. Run locally:
   - `uvicorn main:app --reload`
5. Expose local server using a tunnel (for example `ngrok`) and copy the public URL.
6. In your GitHub repository:
   - Settings -> Webhooks -> Add webhook
   - Payload URL: `https://your-public-url/webhook/github`
   - Content type: `application/json`
   - Secret: same value as `GITHUB_WEBHOOK_SECRET`
   - Events: select "Let me select individual events" -> `Pull requests`
7. Open or update a PR to trigger the bot.

## Run Locally

1. `cd intermediate/code-reviewer-bot`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Fill required env variables
7. `uvicorn main:app --reload`

## Run Tests

- `pytest tests/ -q`
