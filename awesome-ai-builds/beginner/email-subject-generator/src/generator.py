"""Few-shot prompt and structured parsing utilities."""

from __future__ import annotations

import json  # Import json so parser can handle strict JSON model outputs.
import re  # Import regex for fallback parsing of numbered/bulleted lists.

from llm import generate_text  # Import provider-agnostic generation helper from local adapter.

FEW_SHOT_EXAMPLES = [  # Define representative examples to steer output style and tone.
    {
        "body": "Hi team, we are shipping the mobile performance update this Friday. Please review the rollout notes.",
        "subjects": [
            "Mobile Performance Update Ships Friday",
            "Rollout Notes: Mobile Performance Release",
            "Friday Launch: Mobile Speed Improvements",
            "Please Review: Mobile Performance Rollout",
            "Upcoming Release: Mobile Performance Update",
        ],
    },
    {
        "body": "Reminder that invoices for March are due by Monday. Reply if you need deadline support.",
        "subjects": [
            "Reminder: March Invoices Due Monday",
            "Action Needed: Submit March Invoices by Monday",
            "Invoice Deadline Reminder for March",
            "March Billing: Final Submission by Monday",
            "Please Submit March Invoices by Monday",
        ],
    },
]  # Keep examples concise so prompt remains lightweight and focused.


def build_prompt(email_body: str) -> str:
    """Build few-shot prompt requesting structured output."""

    if not email_body.strip():  # Validate body early to avoid wasting provider calls.
        raise ValueError("Email body cannot be empty.")  # Raise clear input validation guidance.
    example_blocks: list[str] = []  # Collect serialized few-shot examples for prompt body.
    for index, sample in enumerate(FEW_SHOT_EXAMPLES, start=1):  # Iterate with indices for readable prompt sections.
        subjects_json = json.dumps(sample["subjects"], ensure_ascii=True)  # Serialize example subjects as JSON to teach exact output format.
        example_blocks.append(  # Append one structured demonstration block per example.
            f"Example {index}\n"  # Mark example boundary for model clarity.
            f"Email Body: {sample['body']}\n"  # Include source email body in demonstration.
            f"Output JSON: {{\"subjects\": {subjects_json}}}"  # Show expected JSON schema explicitly.
        )
    examples = "\n\n".join(example_blocks)  # Combine examples into contiguous training context.
    return (  # Return final few-shot prompt string.
        "Generate exactly five compelling email subject lines.\n"  # Define task scope and quantity requirement.
        "Return valid JSON with this exact schema: {\"subjects\": [\"...\", \"...\", \"...\", \"...\", \"...\"]}\n"  # Enforce strict machine-parseable format.
        "Do not include extra keys.\n\n"  # Prevent noisy extra output.
        f"{examples}\n\n"  # Insert few-shot demonstrations.
        f"Email Body: {email_body.strip()}\n"  # Insert user-provided email body.
        "Output JSON:"  # Prompt model to respond with JSON immediately.
    )


def parse_subjects(raw_output: str) -> list[str]:
    """Parse model output into exactly five subject lines."""

    text = raw_output.strip()  # Normalize whitespace for consistent parsing behavior.
    if not text:  # Guard against empty model output.
        raise ValueError("Model output was empty.")  # Raise clear parsing failure for caller troubleshooting.

    try:  # Attempt strict JSON parsing first because it is the preferred output format.
        data = json.loads(text)  # Parse model text as JSON object.
        subjects = data.get("subjects", []) if isinstance(data, dict) else []  # Extract subjects list safely.
        cleaned = [str(item).strip() for item in subjects if str(item).strip()]  # Normalize list entries and drop blanks.
    except json.JSONDecodeError:  # Fallback when model returns plain text lists instead of JSON.
        lines = [line.strip() for line in text.splitlines() if line.strip()]  # Split non-empty lines for list parsing.
        cleaned = []  # Collect parsed subject candidates from fallback logic.
        for line in lines:  # Iterate over each line to capture numbered or bulleted items.
            candidate = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()  # Remove leading bullets/numbers before storing text.
            if candidate:  # Keep only non-empty parsed candidates.
                cleaned.append(candidate)  # Append normalized subject candidate.

    deduped: list[str] = []  # Build de-duplicated subject list while preserving order.
    for subject in cleaned:  # Iterate in order to keep strongest model suggestions first.
        if subject not in deduped:  # Skip duplicates for cleaner output variety.
            deduped.append(subject)  # Append first occurrence of each unique subject.
    top_five = deduped[:5]  # Keep only first five suggestions to satisfy project contract.
    if len(top_five) < 5:  # Fill missing values when model returns fewer than five options.
        while len(top_five) < 5:  # Continue until output reaches required list length.
            top_five.append(f"Subject Idea {len(top_five) + 1}")  # Add deterministic fallback item for consistent return shape.
    return top_five  # Return exactly five subject lines.


def generate_subjects(email_body: str) -> list[str]:
    """Generate five subject suggestions from email body text."""

    prompt = build_prompt(email_body)  # Build few-shot structured prompt from user email body.
    raw_output = generate_text(  # Request model completion through provider-agnostic adapter.
        prompt=prompt,  # Send task-specific prompt with examples and strict schema instruction.
        system_prompt="You are a concise marketing copywriter and JSON formatter.",  # Encourage concise subject style and valid JSON.
        temperature=0.5,  # Allow moderate creativity for diverse yet relevant subject lines.
        max_tokens=350,  # Keep output compact and easy to parse.
    )
    return parse_subjects(raw_output)  # Parse and normalize generated output into fixed-length list.
