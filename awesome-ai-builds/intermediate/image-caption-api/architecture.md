# Architecture

This service separates HTTP concerns from model inference logic.

## Data Flow

```mermaid
flowchart LR
  A["Image Upload Request"] --> B["FastAPI Route /caption"]
  B --> C["Payload Validation"]
  C --> D["src/caption_service.generate_caption"]
  D --> E["BLIP-2 Processor + Model Inference"]
  E --> F["Caption Text"]
  F --> G["JSON Response"]
```

FastAPI handles request validation and response shaping, while `caption_service.py` owns model loading and caption generation.
