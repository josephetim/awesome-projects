"""FastAPI entrypoint for image caption service."""

from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile  # Import FastAPI primitives for API routing and validation.

from src.caption_service import generate_caption, model_name  # Import caption generation service and model metadata helper.

app = FastAPI(title="Image Caption API", version="1.0.0")  # Create FastAPI application object with metadata.


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health and configured model metadata."""

    return {"status": "ok", "model": model_name()}  # Provide basic health signal and active model identifier.


@app.post("/caption")
async def caption(file: UploadFile = File(...)) -> dict[str, str]:
    """Accept image upload and return generated caption."""

    if not file.content_type or not file.content_type.startswith("image/"):  # Validate MIME type to ensure endpoint receives image payloads.
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")  # Return client error for invalid file type.
    payload = await file.read()  # Read uploaded file bytes from request stream.
    try:  # Handle predictable validation/runtime failures from caption service.
        text = generate_caption(payload)  # Generate caption text from raw image bytes.
    except ValueError as exc:  # Catch known user-input validation errors.
        raise HTTPException(status_code=400, detail=str(exc)) from exc  # Convert to HTTP 400 for clear API feedback.
    except Exception as exc:  # Catch unexpected model/runtime errors.
        raise HTTPException(status_code=500, detail=f"Caption generation failed: {exc}") from exc  # Return HTTP 500 with diagnostic message.
    return {"caption": text}  # Return caption payload as JSON object.
