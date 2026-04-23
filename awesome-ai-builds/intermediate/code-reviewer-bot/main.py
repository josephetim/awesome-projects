"""FastAPI webhook server for automated pull request reviews."""

from __future__ import annotations

import os  # Import os to read GitHub token and webhook secret from environment.

from dotenv import load_dotenv  # Import dotenv for local environment loading.
from fastapi import FastAPI, Header, HTTPException, Request  # Import FastAPI primitives for webhook handling.

from src.reviewer import (  # Import core webhook processing helpers.
    fetch_pull_request_context,
    generate_review_comment,
    post_review_comment,
    verify_signature,
)

load_dotenv()  # Load .env values at startup so runtime secrets are available.

app = FastAPI(title="Code Reviewer Bot", version="1.0.0")  # Create FastAPI app with descriptive metadata.


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health."""

    return {"status": "ok"}  # Return minimal health signal for uptime checks.


@app.post("/webhook/github")
async def github_webhook(
    request: Request,  # Receive raw request for payload and headers.
    x_github_event: str = Header(default=""),  # Read GitHub event type header.
    x_hub_signature_256: str = Header(default=""),  # Read GitHub webhook signature header.
) -> dict[str, str]:
    """Process pull request webhook and post structured review comment."""

    payload = await request.body()  # Read raw webhook payload bytes for signature verification.
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "").strip()  # Read configured webhook secret from environment.
    if secret and not verify_signature(payload, x_hub_signature_256, secret):  # Verify signature when secret is configured.
        raise HTTPException(status_code=401, detail="Invalid webhook signature.")  # Reject unauthenticated webhook payloads.

    if x_github_event != "pull_request":  # Ignore non-pull-request events for predictable bot scope.
        return {"status": "ignored", "reason": "unsupported_event"}  # Return explicit ignored status for observability.

    data = await request.json()  # Parse JSON payload for PR metadata extraction.
    action = str(data.get("action", "")).lower()  # Read webhook action field and normalize case.
    if action not in {"opened", "reopened", "synchronize"}:  # Process only actions that represent review-worthy code changes.
        return {"status": "ignored", "reason": f"unsupported_action:{action}"}  # Return ignored status for unsupported actions.

    repo_full_name = str(data.get("repository", {}).get("full_name", "")).strip()  # Extract owner/repo identifier from payload.
    pull_number = int(data.get("pull_request", {}).get("number", 0) or 0)  # Extract pull request number from payload.
    if not repo_full_name or pull_number <= 0:  # Validate required routing context before API calls.
        raise HTTPException(status_code=400, detail="Payload missing repository or pull request number.")  # Reject malformed webhook payload.

    github_token = os.getenv("GITHUB_TOKEN", "").strip()  # Read GitHub token required for PR read/write operations.
    if not github_token:  # Validate token presence before GitHub API usage.
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN is not configured.")  # Return server config error if token missing.

    context = fetch_pull_request_context(repo_full_name, pull_number, github_token)  # Fetch PR metadata and aggregated diff text.
    if not context["diff"]:  # Skip review comment when no text diff is available.
        return {"status": "ignored", "reason": "no_diff_patch"}  # Return explicit reason for skipping review.

    comment = generate_review_comment(context["title"], context["body"], context["diff"])  # Generate structured review comment via LLM adapter.
    post_review_comment(repo_full_name, pull_number, github_token, comment)  # Post generated review back to PR as issue comment.
    return {"status": "review_posted"}  # Return success status after comment creation.
