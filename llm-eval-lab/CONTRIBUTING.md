# Contributing to llm-eval-lab

This repository accepts evaluation modules that are runnable, measurable, and documented for reproducible learning.

## How To Add a Module

1. Choose a category directory:
   - `foundations/`
   - `metrics/`
   - `frameworks/`
   - `case-studies/`
   - `human-eval/`
2. Create your module folder and include:
   - `README.md`
   - `.env.example`
   - `requirements.txt`
   - `src/`
   - `tests/`
   - `EXTEND.md`
   - `TROUBLESHOOT.md`
   - `architecture.md`
   - `llm.py` only if the module calls an external LLM
3. Provide at least one runnable test.
4. Document metrics and interpretation limits.
5. Update root `README.md` module index table.

## LLM Module Rules

- Use project-level `llm.py` as the only provider integration point.
- Support only `gemini` and `openai`.
- Default to `PROVIDER=gemini`.
- Never import model SDKs directly in other files.

## Pull Request Checklist

- [ ] Module runs with documented commands
- [ ] Tests pass locally
- [ ] Evaluation outputs are reproducible
- [ ] Architecture diagram is present
- [ ] README explains limitations and failure modes
