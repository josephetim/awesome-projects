# Packet Analyzer

## Ethics Boundary

Capture traffic only on networks and interfaces you are authorized to monitor.

- Never sniff traffic on unauthorized networks.
- Use this tool for defensive visibility and learning.

## Skill Level

`intermediate`

## Stack

- Python
- Scapy
- Rich

## What It Does

- Captures live packets from selected interface
- Displays protocol, source, destination, and ports in real time

## Permissions

Packet capture usually requires elevated privileges.

- Linux/macOS: `sudo`
- Windows: run terminal as Administrator (or use Npcap with proper permissions)

## Run

```bash
sudo python sniffer.py --iface eth0
```

Optional:

```bash
sudo python sniffer.py --iface eth0 --count 20
```

## Run Tests

- `pytest tests/ -q`
