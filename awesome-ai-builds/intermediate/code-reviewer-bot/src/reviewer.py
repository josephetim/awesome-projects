"""Webhook review helpers for PR diff analysis and comment posting."""

from __future__ import annotations

import hashlib  # Import hashlib for secure HMAC digest generation.
import hmac  # Import hmac for webhook signature verification.
from typing import Iterable  # Import Iterable for typed patch aggregation utility.

from llm import generate_text  # Import local LLM adapter for provider-isolated model calls.


def verify_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    """Verify GitHub webhook signature using HMAC SHA-256."""

    if not signature_header or not signature_header.startswith("sha256="):  # Validate signature header format expected by GitHub.
        return False  # Return False immediately when signature header is missing or malformed.
    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()  # Compute expected SHA-256 digest using shared secret.
    received = signature_header.split("=", maxsplit=1)[1]  # Extract digest value from header prefix format.
    return hmac.compare_digest(expected, received)  # Use constant-time comparison to prevent timing attacks.


def aggregate_diff_patches(files: Iterable[object], max_chars: int = 18000) -> str:
    """Combine patch snippets from changed files into bounded diff text."""

    lines: list[str] = []  # Collect per-file patch sections in one list for deterministic ordering.
    current_size = 0  # Track accumulated character count to enforce prompt size limit.
    for file in files:  # Iterate changed file objects returned by GitHub pull request API.
        filename = getattr(file, "filename", "unknown_file")  # Read filename safely from file object.
        patch = getattr(file, "patch", "") or ""  # Read unified diff patch content with empty fallback.
        if not patch:  # Skip binary-only or metadata-only changes without patch text.
            continue  # Continue to next file because no meaningful diff text exists.
        section = f"\n### File: {filename}\n{patch}\n"  # Build section with file header for reviewer context.
        if current_size + len(section) > max_chars:  # Enforce max prompt size to keep model calls reliable.
            break  # Stop adding sections once configured character budget is exceeded.
        lines.append(section)  # Append section to final diff payload.
        current_size += len(section)  # Update running size counter.
    return "\n".join(lines).strip()  # Return joined diff text for prompt construction.


def fetch_pull_request_context(repo_full_name: str, pull_number: int, github_token: str) -> dict[str, str]:
    """Fetch PR metadata and diff text from GitHub."""

    from github import Github  # Import PyGithub lazily so unit tests can run without optional dependency installed.

    github = Github(github_token)  # Initialize authenticated GitHub API client.
    repo = github.get_repo(repo_full_name)  # Resolve repository object from owner/name identifier.
    pull = repo.get_pull(pull_number)  # Fetch pull request object by number.
    diff_text = aggregate_diff_patches(pull.get_files())  # Aggregate changed file patches into bounded diff payload.
    return {  # Return normalized context dictionary for prompt construction.
        "title": pull.title or "",  # Include PR title for reviewer context.
        "body": pull.body or "",  # Include PR description for intent understanding.
        "diff": diff_text,  # Include bounded unified diff text.
    }


def build_review_prompt(title: str, body: str, diff: str) -> str:
    """Build structured review prompt with explicit categories."""

    return (  # Return full prompt string for review generation.
        "Review this pull request diff and provide feedback in markdown.\n"  # Define review task and output format.
        "Use these sections exactly:\n"  # Require deterministic section headings for consistent comments.
        "1) Correctness\n"  # Request correctness-focused findings.
        "2) Risks\n"  # Request reliability and security risk notes.
        "3) Readability\n"  # Request maintainability guidance.
        "4) Tests\n"  # Request test coverage observations.
        "5) Suggested Next Actions\n\n"  # Request prioritized actionable follow-ups.
        f"PR Title:\n{title}\n\n"  # Inject pull request title context.
        f"PR Description:\n{body}\n\n"  # Inject pull request description context.
        f"Diff:\n{diff}\n\n"  # Inject aggregated diff payload.
        "Focus on concrete, high-impact issues and avoid generic praise."  # Bias model toward specific actionable review findings.
    )


def generate_review_comment(title: str, body: str, diff: str) -> str:
    """Generate review comment text from PR context."""

    prompt = build_review_prompt(title=title, body=body, diff=diff)  # Build structured prompt from pull request metadata and diff.
    return generate_text(  # Generate review text via local provider adapter.
        prompt=prompt,  # Send review prompt.
        system_prompt="You are a strict but constructive staff engineer performing code review.",  # Set review persona and quality bar.
        temperature=0.1,  # Keep output deterministic and consistent for automation workflows.
        max_tokens=950,  # Allow enough space for all required review sections.
    )


def post_review_comment(repo_full_name: str, pull_number: int, github_token: str, comment: str) -> None:
    """Post generated review comment to GitHub pull request."""

    from github import Github  # Import PyGithub lazily so prompt/unit tests do not require this package at import time.

    github = Github(github_token)  # Initialize authenticated GitHub client for comment posting.
    repo = github.get_repo(repo_full_name)  # Resolve repository object from full name.
    pull = repo.get_pull(pull_number)  # Fetch pull request object by number.
    pull.create_issue_comment(comment)  # Create top-level PR issue comment with generated review text.
