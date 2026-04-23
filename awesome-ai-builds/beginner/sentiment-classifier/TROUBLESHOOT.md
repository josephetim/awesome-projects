# TROUBLESHOOT

## Slow first run

- The model downloads on first startup.
- Keep internet enabled until initial download completes.

## `ModuleNotFoundError: transformers`

- Run `pip install -r requirements.txt`.
- Activate the correct virtual environment before running `python app.py`.

## Out-of-memory issues

- Run on CPU with smaller batch sizes.
- Close other heavy applications.
