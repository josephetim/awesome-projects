# Port Scanner

## Ethics and Legal Boundary

Use this scanner only on systems and networks you are explicitly authorized to test.

- Unauthorized scanning can be illegal and disruptive.
- This tool is for defensive learning and lab environments.

## Skill Level

`intermediate`

## Stack

- Python
- socket
- threading / concurrent futures
- argparse
- Rich

## Features

- single host scan
- CIDR range support
- optional banner grabbing
- JSON export
- CSV export

## Run

```bash
python scanner.py --target 127.0.0.1 --ports 1-1024 --threads 200
```

```bash
python scanner.py --target 192.168.1.0/30 --ports 22,80,443 --banner --json-out scan.json --csv-out scan.csv
```

## Run Tests

- `pytest tests/ -q`
