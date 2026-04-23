# TROUBLESHOOT

## YAML parse errors

- Validate indentation and list syntax in `tests/cases.yaml`.
- Keep scalar values quoted when they include `:` characters.

## Flaky judge results

- Set `temperature=0.0` for both generation and judge calls.
- Tighten judge rubric to explicit PASS/FAIL criteria.

## Provider setup issues

- Ensure `.env` has `PROVIDER=gemini` or `PROVIDER=openai`.
- Set matching API key env variables for selected provider.
