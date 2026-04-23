# Architecture

This module separates payload generation, safe request execution, and defensive query patterns.

## Data Flow

```mermaid
flowchart LR
  A["Demo Script"] --> B["Payload Generator"]
  B --> C["Safe Local Target Check"]
  C --> D["DVWA Request"]
  D --> E["Response Parsing"]
  E --> F["Observation Output"]
  G["defense_examples.py"] --> H["Parameterized Query Pattern"]
```

The offensive demonstrations remain restricted to local lab targets and are paired with defensive implementation examples.
