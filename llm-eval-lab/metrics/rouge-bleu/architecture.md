# Architecture

This module computes ROUGE and BLEU from reference/candidate pairs and surfaces interpretation guidance in a notebook.

## Data Flow

```mermaid
flowchart LR
  A["Reference + Candidate Text"] --> B["ROUGE Scorer"]
  A --> C["BLEU Scorer"]
  B --> D["Metric Table"]
  C --> D
  D --> E["Notebook Interpretation"]
```

The architecture intentionally combines computation with explanatory context to reduce metric misuse.
