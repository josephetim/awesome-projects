# Lab Setup

This module creates a safe local lab for security exercises.

## What It Starts

- DVWA on `http://localhost:8080`
- Ubuntu container for network experimentation

## First-Time Setup (Under 10 Steps)

1. Install Docker Desktop.
2. Open terminal in `lab-setup/`.
3. Run: `docker compose up -d`.
4. Confirm containers: `docker compose ps`.
5. Open DVWA at `http://localhost:8080`.
6. Complete DVWA setup page and login.
7. Enter Ubuntu lab container: `docker exec -it security-lab-ubuntu bash`.
8. Stop lab when done: `docker compose down`.

## Safety Boundaries

- Use this lab only on your local machine.
- Do not point scripts to real external systems.
