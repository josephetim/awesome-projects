# Email Subject Generator

`email-subject-generator` takes an email body and returns five subject line suggestions.

## Why This Exists

This project teaches two core LLM application patterns:

- few-shot prompting for consistent style
- structured parsing for reliable downstream output

## Skill Level

`beginner`

## Stack

- Python
- Streamlit
- python-dotenv
- local provider adapter (`llm.py`)

## Input and Output

- Input: plain text email body
- Output: list of exactly five subject line suggestions

## Provider Setup (Gemini Default)

- Free default path: `PROVIDER=gemini`
- Optional paid upgrade: `PROVIDER=openai`

### API Keys

- Gemini key (free tier available) in `GEMINI_API_KEY`
- OpenAI key (paid) in `OPENAI_API_KEY`

## Run Locally

1. `cd beginner/email-subject-generator`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Fill key values in `.env`
7. `python app.py`

## Run Tests

- `pytest tests/ -q`

## Notes

- Parsing logic is resilient to both JSON and bullet-list model outputs.
- The app enforces exactly five suggestions for a predictable user experience.
