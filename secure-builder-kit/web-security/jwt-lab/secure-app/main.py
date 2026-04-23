"""Secure JWT demo app showing corrected verification patterns."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query  # Import FastAPI primitives.

from src.jwt_utils import issue_rs256, issue_strong_hs256, safe_verify  # Import secure JWT utilities.

app = FastAPI(title="Secure JWT App", version="1.0.0")  # Create secure demo FastAPI app.


@app.get("/health")
def health() -> dict[str, str]:
    """Return health status."""

    return {"status": "ok", "mode": "secure"}  # Return secure app health payload.


@app.get("/secure/hs256/issue")
def issue_secure_hs() -> dict[str, str]:
    """Issue HS256 token with strong secret."""

    token = issue_strong_hs256({"sub": "student", "role": "user"})  # Issue secure HS256 token.
    return {"token": token}  # Return secure token.


@app.get("/secure/hs256/protected")
def protected_secure_hs(token: str = Query(..., description="JWT token")) -> dict:
    """Protected endpoint with strict HS256 verification."""

    ok, value = safe_verify(token, "hs256")  # Verify token in secure HS256 mode.
    if not ok:  # Reject invalid tokens.
        raise HTTPException(status_code=401, detail=str(value))  # Return unauthorized for verification failure.
    return {"access": "granted", "claims": value}  # Return claims for valid secure token.


@app.get("/secure/rs256/issue")
def issue_secure_rs() -> dict[str, str]:
    """Issue RS256 token for secure asymmetric verification."""

    token = issue_rs256({"sub": "student", "role": "user"})  # Issue secure RS256 token.
    return {"token": token}  # Return secure RS256 token.


@app.get("/secure/rs256/protected")
def protected_secure_rs(token: str = Query(..., description="JWT token")) -> dict:
    """Protected endpoint with strict RS256 verification."""

    ok, value = safe_verify(token, "rs256")  # Verify token in secure RS256 mode.
    if not ok:  # Reject invalid tokens.
        raise HTTPException(status_code=401, detail=str(value))  # Return unauthorized for verification failure.
    return {"access": "granted", "claims": value}  # Return claims for valid secure token.
