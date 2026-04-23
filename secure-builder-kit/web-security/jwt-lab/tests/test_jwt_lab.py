"""Tests for vulnerable and secure JWT utility behavior."""

import pytest  # Import pytest for exception assertions and conditional dependency checks.

from src.jwt_utils import (  # Import JWT helpers under test.
    create_none_token,
    public_key_as_hmac_secret,
    secure_decode_hs256,
    vulnerable_decode_confusion,
    vulnerable_decode_none,
)


def test_vulnerable_decode_none_accepts_unsigned_token() -> None:
    """Vulnerable none decoder should trust unsigned token claims."""

    token = create_none_token({"sub": "attacker", "role": "admin"})  # Forge unsigned token with elevated claims.
    claims = vulnerable_decode_none(token)  # Decode without signature verification in vulnerable path.
    assert claims["role"] == "admin"  # Verify vulnerable path accepts forged elevated claim.


def test_secure_decode_hs256_rejects_none_token() -> None:
    """Secure HS256 path should reject unsigned token."""

    jose = pytest.importorskip("jose")  # Skip jose-dependent test when jose package is unavailable.

    token = create_none_token({"sub": "attacker", "role": "admin"})  # Forge unsigned token for rejection test.
    with pytest.raises(jose.JWTError):  # Expect JWT verification failure.
        secure_decode_hs256(token)  # Verify secure path rejects alg:none token.


def test_vulnerable_confusion_accepts_forged_hs256_token() -> None:
    """Vulnerable confusion path should accept forged HS256 token."""

    jose = pytest.importorskip("jose")  # Skip jose-dependent test when jose package is unavailable.

    forged = jose.jwt.encode({"sub": "attacker", "role": "admin"}, public_key_as_hmac_secret(), algorithm="HS256")  # Forge HS256 token using vulnerable secret derivation.
    claims = vulnerable_decode_confusion(forged)  # Decode token through vulnerable confusion path.
    assert claims["role"] == "admin"  # Verify vulnerability permits forged admin claim.
