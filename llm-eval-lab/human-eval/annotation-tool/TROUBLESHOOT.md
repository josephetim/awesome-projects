# TROUBLESHOOT

## `422 Unprocessable Entity` on form submit

- Ensure all form fields are present and use valid values.
- Relevance, accuracy, and tone must be integers between 1 and 5.

## No agreement score signal

- Fleiss’ Kappa needs multiple ratings per item.
- Collect at least 2-3 annotations per item before interpreting results.

## SQLite file path issues

- Set `DB_PATH` in `.env` to a writable location.
- Ensure the application process has filesystem write permissions.
