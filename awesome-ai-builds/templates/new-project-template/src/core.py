"""Core logic for the project template."""


def transform_text(text: str) -> str:
    """Return a normalized uppercase representation for demonstration."""

    normalized = text.strip()  # Remove leading and trailing spaces so outputs are consistent across inputs.
    if not normalized:  # Guard against empty values so callers get an actionable message.
        raise ValueError("Input text cannot be empty.")  # Raise clear error to teach basic input validation.
    return normalized.upper()  # Convert to uppercase to provide deterministic behavior for starter tests.
