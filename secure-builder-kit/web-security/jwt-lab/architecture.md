# Architecture

This module separates insecure and secure JWT validation paths for side-by-side learning.

## Data Flow

```mermaid
flowchart LR
  A["Client Token"] --> B["Vulnerable App"]
  A --> C["Secure App"]
  B --> D["Unsafe Validation Paths"]
  C --> E["Strict Algorithm + Key Validation"]
  F["Attack Scripts"] --> B
  E --> G["Protected Access"]
```

The vulnerable app intentionally demonstrates anti-patterns, while the secure app enforces best-practice verification.
