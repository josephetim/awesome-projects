# Contributing to awesome-ai-builds

This repository accepts production-ready AI projects that are reproducible, tested, and documented for real learners.

## Contribution Flow

1. Fork the repository and create a branch: `feature/your-project-name`.
2. Copy `templates/new-project-template/` into the right level directory:
   - `beginner/`
   - `intermediate/`
   - `advanced/`
3. Rename the copied folder to your project slug (for example `my-rag-app`).
4. Replace template content with your working implementation.
5. Ensure the project includes:
   - `README.md`
   - `.env.example`
   - `requirements.txt`
   - `src/`
   - `tests/`
   - `EXTEND.md`
   - `TROUBLESHOOT.md`
   - `architecture.md`
   - `llm.py` only if the project calls an LLM
6. Run tests from the project root: `pytest tests/`.
7. Update the root `README.md` project index table.
8. Open a pull request with:
   - project purpose
   - setup commands
   - test evidence
   - architecture summary

## Provider Rules for LLM Projects

- Use exactly two providers in project-level `llm.py`: `gemini` and `openai`.
- Default provider must be `gemini`.
- Select provider using `.env` via `PROVIDER=`.
- Never import AI SDKs directly outside `llm.py`.

## Code Quality Expectations

- No placeholder functions.
- No TODO-only submissions.
- Clear naming and modular code.
- Helpful inline comments on non-trivial logic.
- Beginner-friendly README with accurate commands.

## Pull Request Checklist

- [ ] Project runs with documented commands.
- [ ] Tests pass locally.
- [ ] `.env.example` is present and complete.
- [ ] `architecture.md` includes a Mermaid diagram.
- [ ] `EXTEND.md` and `TROUBLESHOOT.md` are practical and specific.
- [ ] If LLM-based, provider logic is isolated in `llm.py`.
