# Architecture

The app uses a deterministic post-processing layer so UI output always contains exactly five subject suggestions.

## Data Flow

```mermaid
flowchart LR
  A["Email Body Input"] --> B["Few-shot Prompt Builder"]
  B --> C["llm.py Provider Adapter"]
  C --> D["Model Output"]
  D --> E["Structured Parser"]
  E --> F["Five Subject Suggestions"]
  F --> G["Streamlit UI"]
```

Input text is transformed into a few-shot prompt, generated through the provider adapter, parsed into structured output, and displayed in Streamlit.
