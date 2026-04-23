# TROUBLESHOOT

## Safety check error

- Set `DVWA_BASE_URL` to `http://localhost:8080` or `http://127.0.0.1:8080`.

## 403 or no expected behavior in DVWA

- Log in to DVWA and set security level to low for training.
- Confirm endpoint path matches your DVWA version.

## Time-based demo shows no delay

- Ensure target DB supports sleep function in lab context.
- Network jitter can obscure small timing differences.
