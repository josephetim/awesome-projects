# secure-builder-kit

`secure-builder-kit` is an educational cybersecurity repository focused on defensive learning in authorized lab environments.

## Authorized-Use Only

This repository is strictly for legal, defensive, and educational use.

- Use only against:
  - DVWA in local lab setup
  - intentionally vulnerable local demos in this repo
  - explicit environments you are authorized to test
- Never target real systems without written permission.

## Why This Exists

Beginners and builders often need safe, practical labs that connect theory to real workflows without crossing legal or ethical boundaries.

## Module Index

| Area | Module | Skill Level | Stack | Description |
|---|---|---|---|---|
| lab setup | `lab-setup` | beginner | Docker Compose | Spins up DVWA + Ubuntu lab containers locally. |
| foundations | `networking-basics` | beginner | Python, socket, requests, dnspython, notebook | Interactive scripts for DNS, TCP handshake, and HTTP anatomy. |
| web security | `owasp-top-10` | intermediate | Python + DVWA/local demos | Category-by-category defensive walkthroughs with safe demo scripts. |
| web security | `sql-injection` | intermediate | Python, requests, BeautifulSoup, DVWA | Deep SQLi walkthrough with safe lab-only payload testing and defenses. |
| web security | `jwt-lab` | advanced | Python, FastAPI, python-jose, Docker | Vulnerable JWT patterns, exploit demos, and secure fixes. |
| network security | `packet-analyzer` | intermediate | Python, Scapy, Rich | Real-time packet inspection with protocol breakdown. |
| tools | `port-scanner` | intermediate | Python, socket, threading, argparse, Rich | Safe TCP scanner with CIDR, banner grab, and export support. |

## Ethics and Safety

Read [ETHICS.md](ETHICS.md) before running any module.

## Repository Layout

```text
secure-builder-kit/
├── README.md
├── CONTRIBUTING.md
├── ETHICS.md
├── lab-setup/
├── foundations/networking-basics/
├── web-security/
├── network-security/packet-analyzer/
├── tools/port-scanner/
├── ctf-writeups/README.md
└── resources/certifications/README.md
```
