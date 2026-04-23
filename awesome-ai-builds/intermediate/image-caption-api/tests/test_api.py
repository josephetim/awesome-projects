"""API tests for image caption service."""

from fastapi.testclient import TestClient  # Import TestClient for HTTP-style endpoint testing.

import main  # Import API module so tests target real FastAPI app object.

client = TestClient(main.app)  # Instantiate reusable test client bound to the app.


def test_health_endpoint() -> None:
    """Health endpoint should return service status."""

    response = client.get("/health")  # Call health endpoint.
    assert response.status_code == 200  # Ensure endpoint returns success.
    assert response.json()["status"] == "ok"  # Ensure response payload includes expected status value.


def test_caption_rejects_non_image_upload() -> None:
    """Caption endpoint should reject non-image content types."""

    response = client.post("/caption", files={"file": ("notes.txt", b"text", "text/plain")})  # Send invalid content type upload.
    assert response.status_code == 400  # Ensure API rejects invalid input type.
    assert "image" in response.json()["detail"].lower()  # Ensure error message explains required image type.
