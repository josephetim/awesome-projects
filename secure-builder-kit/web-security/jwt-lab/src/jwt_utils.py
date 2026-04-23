"""JWT helpers for vulnerable and secure demo apps."""

from __future__ import annotations

import base64  # Import base64 for manual JWT segment encoding/decoding.
import json  # Import json for token payload serialization.
import time  # Import time for expiration claim timestamps.

WEAK_SECRET = "password123"  # Intentionally weak secret for vulnerability demonstration.
STRONG_SECRET = "9C0fJq1#Xv7!4sA2nL8pRm5@tW3dEe"  # Strong secret for secure HS256 flow.


def _require_jose():
    """Import jose.jwt lazily and fail with clear guidance when missing."""

    try:  # Attempt jose import only when JWT crypto operations are requested.
        from jose import jwt  # Import jose.jwt lazily so non-crypto tests can run without dependency.

        return jwt  # Return imported module object for caller use.
    except ModuleNotFoundError as exc:  # Catch missing dependency error.
        raise RuntimeError("python-jose is required for this JWT operation. Install requirements.txt.") from exc  # Raise actionable runtime guidance.


def _generate_rsa_pair() -> tuple[str, str]:
    """Generate RSA key pair for RS256 demos, with fallback placeholders."""

    try:  # Attempt cryptography-backed key generation.
        from cryptography.hazmat.primitives import serialization  # Import serialization lazily for PEM conversion.
        from cryptography.hazmat.primitives.asymmetric import rsa  # Import RSA keygen lazily.

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)  # Generate private RSA key object.
        private_pem = private_key.private_bytes(  # Serialize private key to PEM bytes.
            encoding=serialization.Encoding.PEM,  # Use PEM encoding for jose compatibility.
            format=serialization.PrivateFormat.PKCS8,  # Use PKCS8 key format.
            encryption_algorithm=serialization.NoEncryption(),  # Keep unencrypted for local educational lab.
        ).decode("utf-8")  # Decode private key bytes into UTF-8 text.
        public_pem = private_key.public_key().public_bytes(  # Serialize public key to PEM bytes.
            encoding=serialization.Encoding.PEM,  # Use PEM encoding.
            format=serialization.PublicFormat.SubjectPublicKeyInfo,  # Use SPKI public key format.
        ).decode("utf-8")  # Decode public key bytes into UTF-8 text.
        return private_pem, public_pem  # Return generated PEM key strings.
    except ModuleNotFoundError:  # Handle missing cryptography dependency.
        return "MISSING_PRIVATE_KEY", "MISSING_PUBLIC_KEY"  # Return placeholders that surface dependency issue when RS256 is used.


RSA_PRIVATE_KEY, RSA_PUBLIC_KEY = _generate_rsa_pair()  # Initialize key material once at import time.


def _now_exp(minutes: int = 30) -> int:
    """Return Unix timestamp for expiration claim."""

    return int(time.time()) + (minutes * 60)  # Compute expiration timestamp in seconds.


def _b64url_encode_json(value: dict) -> str:
    """Encode dictionary as base64url JSON segment."""

    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")  # Serialize JSON object compactly.
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("utf-8")  # Return base64url string without padding.


def _b64url_decode_json(segment: str) -> dict:
    """Decode base64url JSON segment into dictionary."""

    padded = segment + ("=" * (-len(segment) % 4))  # Add required base64 padding.
    return json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8"))  # Decode and parse JSON payload.


def create_none_token(claims: dict) -> str:
    """Create unsigned token with alg:none for vulnerability demonstration."""

    header = {"alg": "none", "typ": "JWT"}  # Build unsigned JWT header.
    payload = {**claims, "exp": _now_exp()}  # Add expiration claim to payload.
    return f"{_b64url_encode_json(header)}.{_b64url_encode_json(payload)}."  # Return unsigned JWT string with empty signature.


def issue_weak_hs256(claims: dict) -> str:
    """Issue HS256 token with intentionally weak secret."""

    jwt = _require_jose()  # Load jose module for signed token generation.
    payload = {**claims, "exp": _now_exp()}  # Add expiration claim.
    return jwt.encode(payload, WEAK_SECRET, algorithm="HS256")  # Sign token with weak secret.


def issue_strong_hs256(claims: dict) -> str:
    """Issue HS256 token with strong secret."""

    jwt = _require_jose()  # Load jose module for signed token generation.
    payload = {**claims, "exp": _now_exp()}  # Add expiration claim.
    return jwt.encode(payload, STRONG_SECRET, algorithm="HS256")  # Sign token with strong secret.


def issue_rs256(claims: dict) -> str:
    """Issue RS256 token with generated private key."""

    jwt = _require_jose()  # Load jose module for signed token generation.
    payload = {**claims, "exp": _now_exp()}  # Add expiration claim.
    return jwt.encode(payload, RSA_PRIVATE_KEY, algorithm="RS256")  # Sign token with private RSA key.


def vulnerable_decode_none(token: str) -> dict:
    """Vulnerable decode path that skips signature verification."""

    segments = token.split(".")  # Split JWT into segments.
    if len(segments) < 2:  # Validate minimal JWT structure.
        raise ValueError("Token format is invalid.")  # Raise parse error for malformed token.
    return _b64url_decode_json(segments[1])  # Decode payload segment without signature verification.


def vulnerable_decode_weak(token: str) -> dict:
    """Vulnerable decode path that accepts weak secret."""

    jwt = _require_jose()  # Load jose module lazily.
    return jwt.decode(token, WEAK_SECRET, algorithms=["HS256"])  # Decode using weak secret.


def public_key_as_hmac_secret() -> str:
    """Return flawed HMAC secret derived from RSA public key."""

    return RSA_PUBLIC_KEY.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "")  # Strip PEM markers to produce misuse-prone HMAC key.


def vulnerable_decode_confusion(token: str) -> dict:
    """Vulnerable decode path that allows RS256->HS256 confusion."""

    jwt = _require_jose()  # Load jose module lazily.
    header = jwt.get_unverified_header(token)  # Read JWT header without verification.
    if header.get("alg") == "HS256":  # Accept attacker-selected HS256 algorithm path.
        return jwt.decode(token, public_key_as_hmac_secret(), algorithms=["HS256"])  # Incorrectly verify with public-key-derived HMAC secret.
    return jwt.decode(token, RSA_PUBLIC_KEY, algorithms=["RS256"])  # Verify RS256 tokens with public key.


def secure_decode_hs256(token: str) -> dict:
    """Secure HS256 verification path."""

    jwt = _require_jose()  # Load jose module lazily.
    return jwt.decode(token, STRONG_SECRET, algorithms=["HS256"])  # Verify strict HS256 with strong secret.


def secure_decode_rs256(token: str) -> dict:
    """Secure RS256 verification path."""

    jwt = _require_jose()  # Load jose module lazily.
    return jwt.decode(token, RSA_PUBLIC_KEY, algorithms=["RS256"])  # Verify strict RS256 with public key.


def decode_with_secret(token: str, secret: str) -> dict:
    """Try decode token with provided HS256 secret."""

    jwt = _require_jose()  # Load jose module lazily.
    return jwt.decode(token, secret, algorithms=["HS256"])  # Decode token with caller-provided secret guess.


def safe_verify(token: str, mode: str) -> tuple[bool, dict | str]:
    """Verify token in secure mode and return success flag with payload/error."""

    try:  # Wrap verification flow to return structured success/error tuples.
        if mode == "hs256":  # Select secure HS256 mode.
            return True, secure_decode_hs256(token)  # Return verified claims on success.
        if mode == "rs256":  # Select secure RS256 mode.
            return True, secure_decode_rs256(token)  # Return verified claims on success.
        return False, "Unsupported secure mode."  # Reject unknown mode names.
    except Exception as exc:  # Catch verification/dependency/runtime errors.
        return False, str(exc)  # Return failure payload with error message.
