"""Intentionally vulnerable JWT demo app for local educational use."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query  # Import FastAPI primitives for route handling and validation.

from src.jwt_utils import (  # Import vulnerable JWT utility flows.
    issue_rs256,
    issue_weak_hs256,
    vulnerable_decode_confusion,
    vulnerable_decode_none,
    vulnerable_decode_weak,
)

app = FastAPI(title="Vulnerable JWT App", version="1.0.0")  # Create vulnerable demo FastAPI app.


@app.get("/health")
def health() -> dict[str, str]:
    """Return health status."""

    return {"status": "ok", "mode": "vulnerable"}  # Return health status payload.


@app.get("/vuln/none/issue")
def issue_none() -> dict[str, str]:
    """Issue intentionally unsafe unsigned token (alg:none attack surface)."""

    from src.jwt_utils import create_none_token  # Import none-token helper lazily for clarity.

    token = create_none_token({"sub": "student", "role": "user"})  # Create unsigned token claims for demo.
    return {"token": token}  # Return token to caller.


@app.get("/vuln/none/protected")
def protected_none(token: str = Query(..., description="JWT token")) -> dict:
    """Vulnerable endpoint that trusts unsigned token claims."""

    try:  # Handle malformed token decode errors.
        claims = vulnerable_decode_none(token)  # Decode claims without signature verification.
    except Exception as exc:  # Catch decode exceptions.
        raise HTTPException(status_code=401, detail=str(exc)) from exc  # Return unauthorized error for invalid token.
    return {"access": "granted", "claims": claims}  # Return vulnerable access response with claims.


@app.get("/vuln/weak/issue")
def issue_weak() -> dict[str, str]:
    """Issue token signed with weak HMAC secret."""

    token = issue_weak_hs256({"sub": "student", "role": "user"})  # Issue HS256 token with intentionally weak secret.
    return {"token": token}  # Return weak-secret token.


@app.get("/vuln/weak/protected")
def protected_weak(token: str = Query(..., description="JWT token")) -> dict:
    """Vulnerable endpoint that accepts weak HMAC secret."""

    try:  # Handle JWT verification errors.
        claims = vulnerable_decode_weak(token)  # Decode token using weak shared secret.
    except Exception as exc:  # Catch decode failures.
        raise HTTPException(status_code=401, detail=str(exc)) from exc  # Return unauthorized error for invalid token.
    return {"access": "granted", "claims": claims}  # Return vulnerable access response.


@app.get("/vuln/confusion/issue")
def issue_confusion() -> dict[str, str]:
    """Issue RS256 token for algorithm confusion demonstration."""

    token = issue_rs256({"sub": "student", "role": "user"})  # Issue RS256 token for confusion attack baseline.
    return {"token": token}  # Return RS256 token.


@app.get("/vuln/confusion/protected")
def protected_confusion(token: str = Query(..., description="JWT token")) -> dict:
    """Vulnerable endpoint allowing RS256->HS256 confusion."""

    try:  # Handle decode verification errors.
        claims = vulnerable_decode_confusion(token)  # Decode token in vulnerable confusion mode.
    except Exception as exc:  # Catch decode failures.
        raise HTTPException(status_code=401, detail=str(exc)) from exc  # Return unauthorized for invalid token.
    return {"access": "granted", "claims": claims}  # Return vulnerable access response.
