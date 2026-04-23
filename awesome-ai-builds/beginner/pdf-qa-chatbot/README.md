# PDF QA Chatbot

`pdf-qa-chatbot` lets you upload a PDF, ask questions, retrieve relevant document chunks, and get grounded answers.

## Why This Exists

Beginners often struggle to connect chunking, embeddings, vector search, and prompt construction into one practical workflow.  
This project shows the full retrieval-augmented generation (RAG) path in a single app.

## Skill Level

`beginner`

## Stack

- Python
- LangChain text splitters
- FAISS
- Gradio
- python-dotenv
- Gemini/OpenAI via local `llm.py`

## Input and Output

- Input:
  - a PDF file upload
  - a natural language question
- Output:
  - an answer generated from retrieved PDF chunks
  - context-aware response based on vector search results

## Provider Setup (Gemini Default)

This project uses the project-root `llm.py` adapter only.

- Free default: `PROVIDER=gemini`
- Optional paid upgrade: `PROVIDER=openai`

### Getting API Keys

- Gemini free tier: create a key in Google AI Studio and place it in `GEMINI_API_KEY`.
- OpenAI paid path: create a key in OpenAI dashboard and place it in `OPENAI_API_KEY`.

## Run Locally

1. `cd beginner/pdf-qa-chatbot`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS/Linux)
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Fill API key values in `.env`
7. `python app.py`

## Run Tests

- `pytest tests/ -q`

## File Map

- `app.py`: Gradio UI entrypoint
- `llm.py`: provider adapter (Gemini/OpenAI only)
- `src/pdf_qa.py`: PDF parsing, chunking, indexing, retrieval, prompting
- `tests/test_pdf_qa.py`: unit tests for prompt and source formatting
