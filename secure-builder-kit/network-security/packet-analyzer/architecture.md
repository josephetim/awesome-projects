# Architecture

This module captures packets from a selected interface and renders protocol summaries in real time.

## Data Flow

```mermaid
flowchart LR
  A["Network Interface"] --> B["Scapy Sniffer"]
  B --> C["Packet Summarizer"]
  C --> D["Rich Terminal Renderer"]
```

The pipeline is read-only and designed for defensive observability in authorized environments.
