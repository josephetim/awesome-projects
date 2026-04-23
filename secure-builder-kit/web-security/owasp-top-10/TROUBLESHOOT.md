# TROUBLESHOOT

## Scripts fail with safety error

- Confirm target URL host is `localhost` or `127.0.0.1`.
- These scripts intentionally block non-local targets.

## DVWA path mismatch

- Ensure DVWA is running at `http://localhost:8080`.
- Update module README reproduction steps if your setup differs.

## Request errors

- Check lab containers are running.
- Verify network/firewall rules on your host.
