# Architecture

This template separates user-facing entrypoints from reusable core logic.

## Data Flow

```mermaid
flowchart LR
  A["Input"] --> B["app.py entrypoint"]
  B --> C["src/core.py logic"]
  C --> D["Output"]
```

Input text enters through `app.py`, gets validated and transformed in `src/core.py`, and then returns as output.
