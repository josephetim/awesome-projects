# Architecture

This module combines server-rendered annotation forms with SQLite persistence and agreement computation.

## Data Flow

```mermaid
flowchart LR
  A["Annotator Opens Item"] --> B["FastAPI + Jinja Form"]
  B --> C["Form Submission"]
  C --> D["SQLite Annotation Storage"]
  D --> E["Results Page"]
  E --> F["Fleiss' Kappa Computation"]
```

Human ratings are stored as structured rubric scores, then aggregated into inter-annotator agreement signals for quality analysis.
