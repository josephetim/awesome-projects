# TROUBLESHOOT

## DNS/host resolution errors

- Confirm target host/IP is correct and reachable.
- For CIDR, ensure format is valid (for example `192.168.1.0/24`).

## Scan appears slow

- Reduce port range or increase thread count carefully.
- Network latency and filtered ports increase scan duration.

## Empty results

- Target may have no open ports in provided range.
- Verify host is alive and reachable from your scanner environment.
