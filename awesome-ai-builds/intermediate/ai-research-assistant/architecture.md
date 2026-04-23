# Architecture

This project uses a stateful workflow where one node gathers evidence and another node synthesizes findings.

## Data Flow

```mermaid
flowchart LR
  A["Research Question"] --> B["Search Node (Tavily Tool)"]
  B --> C["State Update: results + sources"]
  C --> D["Synthesis Node (llm.py)"]
  D --> E["Structured Summary"]
  E --> F["Streamlit UI"]
```

State management keeps question, search results, sources, and summary in a single structured object passed between workflow stages.
