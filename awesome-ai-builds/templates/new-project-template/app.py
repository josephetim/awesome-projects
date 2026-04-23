"""Template entrypoint for simple command-line execution."""

from src.core import transform_text  # Import core function so entrypoint stays thin and testable.


def main() -> None:
    """Run a small text transformation demo."""

    sample_input = "template input"  # Define deterministic sample input so new contributors can verify behavior quickly.
    output = transform_text(sample_input)  # Call business logic from src module to preserve separation of concerns.
    print(output)  # Print output for immediate feedback when running `python app.py`.


if __name__ == "__main__":
    main()  # Execute demo only when file is run as a script.
