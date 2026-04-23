# TROUBLESHOOT

## Attack scripts fail with connection errors

- Start vulnerable app on `localhost:8001`.
- Confirm correct endpoint paths from README.

## RS256 confusion demo fails

- Ensure vulnerable app is running the included `vulnerable-app/main.py`.
- Confirm script uses local app only and matching helper key logic.

## Token decode errors in secure app

- Secure app intentionally rejects forged/invalid tokens.
- Issue a fresh token from secure issue endpoints before testing protected routes.
