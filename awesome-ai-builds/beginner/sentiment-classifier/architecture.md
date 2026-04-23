# Architecture

This project keeps inference logic separate from UI code and runs fully locally.

## Data Flow

```mermaid
flowchart LR
  A["Text Input"] --> B["app.py (Gradio)"]
  B --> C["src/classifier.py"]
  C --> D["Local Transformers Pipeline"]
  D --> E["Label Mapping + Confidence"]
  E --> F["JSON Output in UI"]
```

The app receives user text, runs local model inference, applies threshold-based neutral handling, and returns a structured result.
