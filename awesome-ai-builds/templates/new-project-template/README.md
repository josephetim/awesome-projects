# New Project Template

This template gives contributors a clean baseline for adding a new project to `awesome-ai-builds`.

## What This Template Includes

- Working folder structure
- Environment variable example
- Test starter
- Architecture guide with Mermaid
- Extension and troubleshooting docs

## How To Use

1. Copy this folder into `beginner/`, `intermediate/`, or `advanced/`.
2. Rename the folder to your project slug.
3. Update `README.md` with your project details.
4. Keep or remove `llm.py` based on whether the project calls an LLM.
5. Implement code in `src/` and expose a runnable entrypoint.
6. Add tests in `tests/`.
7. Add your module row to the root `README.md` index table.

## Minimum Quality Requirements

- Production-quality code (no placeholder logic)
- At least one passing test
- Accurate setup instructions
- Clear inputs and outputs
- Inline comments on non-trivial logic
