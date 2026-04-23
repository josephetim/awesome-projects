# Architecture

This module provides three independent observational functions for DNS, TCP, and HTTP concepts.

## Data Flow

```mermaid
flowchart LR
  A["User Input (domain/host/url)"] --> B["DNS Lookup Function"]
  A --> C["TCP Handshake Function"]
  A --> D["HTTP Anatomy Function"]
  B --> E["Structured Output"]
  C --> E
  D --> E
```

All functions prioritize explanation and diagnostics rather than offensive behavior.
