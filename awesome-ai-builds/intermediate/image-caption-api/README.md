# Image Caption API

`image-caption-api` exposes a REST endpoint that accepts an image upload and returns a descriptive caption.

## Why This Exists

This module demonstrates how to package local vision-language inference behind a clean API with health checks and testable service boundaries.

## Skill Level

`intermediate`

## Stack

- Python
- FastAPI
- Uvicorn
- Hugging Face BLIP-2
- Pillow

## Input and Output

- Input: image file upload to `POST /caption`
- Output: JSON object containing generated caption text

## Run Locally

1. `cd intermediate/image-caption-api`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `copy .env.example .env` (Windows) or `cp .env.example .env`
6. `uvicorn main:app --reload`

## API Endpoints

- `GET /health`
- `POST /caption` (multipart file upload under field name `file`)

## Example cURL

```bash
curl -X GET http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/caption \
  -F "file=@./example.jpg"
```

## CPU vs GPU Tradeoffs

- CPU:
  - Easier setup and no CUDA dependency
  - Slower inference, especially for larger BLIP-2 variants
- GPU:
  - Faster inference and better throughput
  - Requires CUDA-compatible hardware and matching PyTorch build

For local learning, CPU is acceptable. For frequent inference, GPU is strongly recommended.

## Run Tests

- `pytest tests/ -q`
