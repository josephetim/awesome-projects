# Architecture

This module loads YAML test cases, executes prompts, evaluates outputs by strategy, and reports results through pytest assertions.

## Data Flow

```mermaid
flowchart LR
  A["cases.yaml"] --> B["Case Loader"]
  B --> C["Prompt Execution via llm.py"]
  C --> D["Strategy Evaluator"]
  D --> E["pytest Assertions"]
```

The evaluator supports exact match, contains checks, and LLM-as-judge with explicit PASS/FAIL verdict parsing.
