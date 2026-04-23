# Architecture

This tool expands targets, parses ports, scans concurrently, and exports open-port findings.

## Data Flow

```mermaid
flowchart LR
  A["CLI Target + Ports"] --> B["Target Expansion"]
  A --> C["Port Parsing"]
  B --> D["Concurrent TCP Scan"]
  C --> D
  D --> E["Open Port Results"]
  E --> F["Rich Output"]
  E --> G["JSON/CSV Export"]
```

Concurrency improves scan speed by overlapping network wait time across many sockets.
