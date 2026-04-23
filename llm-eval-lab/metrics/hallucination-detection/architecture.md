# Architecture

This module computes grounding signals entirely locally and aggregates them into an interpretable score set.

## Data Flow

```mermaid
flowchart LR
  A["Source Text + Answer"] --> B["Lexical Overlap"]
  A --> C["Sentence Embedding Similarity"]
  A --> D["BERTScore F1"]
  B --> E["Combined Grounding Report"]
  C --> E
  D --> E
```

The module emphasizes metric interpretation and limitations instead of treating any single score as ground truth.
