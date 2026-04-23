# Sentiment Classifier

`sentiment-classifier` labels text as `positive`, `negative`, or `neutral` and returns a confidence score.

## Why This Exists

This project demonstrates a complete local NLP app with no API calls, which makes it ideal for beginners learning model inference fundamentals.

## Skill Level

`beginner`

## Stack

- Python
- Hugging Face Transformers
- Gradio

## Input and Output

- Input: one text string
- Output: sentiment label (`positive` / `negative` / `neutral`) and confidence score

## API Keys

No API key is required.  
This project runs fully locally using a pre-trained transformer model downloaded from Hugging Face.

## Run Locally

1. `cd beginner/sentiment-classifier`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python app.py`

## Run Tests

- `pytest tests/ -q`

## Notes

- First run may take longer because model weights are downloaded.
- CPU works fine for this project; GPU is optional.
