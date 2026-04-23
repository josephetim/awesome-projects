"""BLIP-2 caption generation service."""

from __future__ import annotations

import io  # Import io to wrap raw bytes into in-memory file-like objects.
import os  # Import os to read runtime model configuration from environment.
from functools import lru_cache  # Cache model loading so each request avoids repeated heavy initialization.
from typing import Any  # Use Any for model/processor typing to avoid hard dependency in static imports.

from dotenv import load_dotenv  # Import dotenv to support local `.env` configuration.
from PIL import Image  # Import Pillow image class for preprocessing uploaded bytes.

load_dotenv()  # Load model configuration values before service functions run.


@lru_cache(maxsize=1)
def _load_model() -> tuple[Any, Any, str]:
    """Load BLIP-2 processor and model once per process."""

    import torch  # Import torch lazily because startup should remain lightweight until first request.
    from transformers import Blip2ForConditionalGeneration, Blip2Processor  # Import BLIP-2 classes lazily for optional heavy dependency.

    model_name = os.getenv("BLIP_MODEL_NAME", "Salesforce/blip2-opt-2.7b").strip()  # Read model name from env with BLIP-2 default.
    requested_device = os.getenv("BLIP_DEVICE", "cpu").strip().lower()  # Read requested device mode from env for deployment flexibility.
    if requested_device == "cuda" and torch.cuda.is_available():  # Respect explicit CUDA request only when GPU is actually available.
        device = "cuda"  # Use GPU for faster inference and lower latency.
    else:  # Fall back to CPU when CUDA is unavailable or not requested.
        device = "cpu"  # Use CPU as robust default path for most local setups.

    processor = Blip2Processor.from_pretrained(model_name)  # Load tokenizer/image processor for selected BLIP-2 model.
    model = Blip2ForConditionalGeneration.from_pretrained(model_name)  # Load pretrained BLIP-2 weights from Hugging Face hub/cache.
    model.to(device)  # Move model weights to selected compute device.
    model.eval()  # Put model in eval mode to disable training-only behavior.
    return processor, model, device  # Return initialized artifacts for cached reuse.


def model_name() -> str:
    """Expose configured model name for health endpoint reporting."""

    return os.getenv("BLIP_MODEL_NAME", "Salesforce/blip2-opt-2.7b").strip()  # Return model identifier used by this service.


def generate_caption(image_bytes: bytes, max_new_tokens: int = 40) -> str:
    """Generate caption text for an uploaded image."""

    if not image_bytes:  # Validate non-empty payload before decoding image bytes.
        raise ValueError("Image payload is empty.")  # Raise clear validation error for API layer.

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Decode image bytes and normalize color space for model compatibility.
    processor, model, device = _load_model()  # Load cached processor/model/device tuple.
    import torch  # Import torch lazily to control no_grad context and device placement.

    inputs = processor(images=image, return_tensors="pt").to(device)  # Convert image to model input tensors and move to target device.
    with torch.no_grad():  # Disable gradient computation to reduce memory usage and speed up inference.
        generated = model.generate(**inputs, max_new_tokens=max_new_tokens)  # Run autoregressive generation to produce caption token IDs.
    caption = processor.batch_decode(generated, skip_special_tokens=True)[0].strip()  # Decode generated token IDs into human-readable text.
    if not caption:  # Validate output text to catch unexpected empty decoding results.
        raise RuntimeError("Model generated an empty caption.")  # Raise explicit error for easier debugging.
    return caption  # Return generated caption string to API handler.
