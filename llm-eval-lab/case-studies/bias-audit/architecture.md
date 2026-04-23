# Architecture

This module executes counterfactual prompt pairs, computes disparity heuristics, and visualizes group-level patterns.

## Data Flow

```mermaid
flowchart LR
  A["Prompt Pair CSV"] --> B["Pair Runner via llm.py"]
  B --> C["Output A / Output B"]
  C --> D["Tone + Length Disparity Scoring"]
  D --> E["Pair-Level Audit Table"]
  E --> F["Group Aggregation"]
  F --> G["Streamlit + Plotly Visualization"]
```

The design supports iterative auditing by keeping prompts, outputs, scores, and grouped summaries explicit.
