# Architecture

This module organizes each OWASP category as a self-contained learning unit with attack simulation and defense example.

## Data Flow

```mermaid
flowchart LR
  A["Category README"] --> B["Safe exploit.py (local lab only)"]
  B --> C["Observed Vulnerability Behavior"]
  C --> D["defense.py Secure Pattern"]
  D --> E["Mitigated Outcome"]
```

Each unit pairs demonstration with mitigation to reinforce defensive engineering practice.
