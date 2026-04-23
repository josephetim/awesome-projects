# Architecture

This module combines retrieval, generation, and evaluation in a single feedback loop.

## Data Flow

```mermaid
flowchart LR
  A["Question"] --> B["Document Loader + Chunker"]
  B --> C["Embedding + FAISS Index"]
  A --> D["Top-k Retrieval"]
  C --> D
  D --> E["Prompt Assembly"]
  E --> F["Answer Generation via llm.py"]
  F --> G["RAGAS / Heuristic Evaluation"]
  G --> H["Streamlit Metrics View"]
```

The architecture is intentionally modular so teams can tune retrieval, prompt style, and evaluation independently.
