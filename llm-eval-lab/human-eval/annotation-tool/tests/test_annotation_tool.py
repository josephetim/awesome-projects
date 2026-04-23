"""Tests for annotation tool metrics and web routes."""

from fastapi.testclient import TestClient  # Import TestClient for route testing.

from src.metrics import fleiss_kappa  # Import Fleiss' Kappa metric helper.
from src.webapp import app  # Import FastAPI app under test.


def test_fleiss_kappa_perfect_agreement() -> None:
    """Fleiss' Kappa should be high for perfect agreement matrix."""

    matrix = [  # Build perfect agreement matrix for 3 items and 3 raters.
        [3, 0, 0, 0, 0],  # Item 1: all raters chose category 1.
        [0, 3, 0, 0, 0],  # Item 2: all raters chose category 2.
        [0, 0, 3, 0, 0],  # Item 3: all raters chose category 3.
    ]
    assert fleiss_kappa(matrix) >= 0.99  # Ensure kappa indicates near-perfect agreement.


def test_home_route_renders(monkeypatch, tmp_path) -> None:
    """Home route should render successfully with temporary DB."""

    db_file = tmp_path / "annotation_test.db"  # Create temporary DB file path for isolated test data.
    monkeypatch.setenv("DB_PATH", str(db_file))  # Point app DB path to temporary file for test isolation.
    with TestClient(app) as client:  # Use context manager so startup events run before request execution.
        response = client.get("/")  # Call home route.
    assert response.status_code == 200  # Ensure home route returns successful status.
    assert "Human Evaluation Annotation Tool" in response.text  # Ensure response contains expected page title text.
