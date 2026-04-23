# Architecture

This module runs a fixed prompt set against both providers, scores each output, and visualizes aggregate and detailed comparisons.

## Data Flow

```mermaid
flowchart LR
  A["Prompt CSV"] --> B["Provider Runner via llm.py"]
  B --> C["Output Scoring Rubric"]
  C --> D["Prompt-Level Results Table"]
  D --> E["Provider Aggregation"]
  E --> F["Streamlit + Plotly Dashboard"]
```

A stable prompt dataset and explicit scoring rubric make provider comparisons reproducible and reviewable.
