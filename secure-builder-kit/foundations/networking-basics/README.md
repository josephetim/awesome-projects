# Networking Basics

This module teaches core networking concepts through safe, observational Python scripts.

## Ethics Boundary

Use these scripts only for learning and diagnostics on systems you own or are authorized to inspect.

- No attack automation is included.
- Scripts are observational only.

## Skill Level

`beginner`

## Stack

- Python
- socket
- requests
- dnspython
- Jupyter notebook

## What It Covers

- DNS lookup flow
- TCP 3-way handshake explanation
- HTTP request anatomy

## Run

1. `cd foundations/networking-basics`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python main.py`
6. Optional notebook: `jupyter notebook networking_basics.ipynb`

## Run Tests

- `pytest tests/ -q`
