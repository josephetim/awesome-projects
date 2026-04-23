# TROUBLESHOOT

## Port 8080 already in use

- Stop conflicting local services.
- Or change host mapping in `docker-compose.yml`.

## DVWA not loading

- Check container status with `docker compose ps`.
- Inspect logs: `docker compose logs dvwa`.

## Ubuntu container exits

- Recreate with `docker compose up -d --force-recreate`.
