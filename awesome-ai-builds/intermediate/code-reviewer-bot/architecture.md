# Architecture

This service receives GitHub webhooks, verifies authenticity, builds a review prompt from PR diff context, and posts a comment back to GitHub.

## Data Flow

```mermaid
flowchart LR
  A["GitHub PR Webhook"] --> B["FastAPI /webhook/github"]
  B --> C["HMAC Signature Verification"]
  C --> D["Fetch PR Metadata + Diff (PyGithub)"]
  D --> E["Prompt Builder"]
  E --> F["llm.py Review Generation"]
  F --> G["Post PR Comment (PyGithub)"]
```

Security-critical logic (signature verification) runs before any expensive processing or outbound API calls.
