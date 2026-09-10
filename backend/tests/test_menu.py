"""
test_menu.py — Tests for the /menu/generate endpoint.

We mock generate_description() so these tests run instantly, need no
internet connection, and never spend real API quota. What we're
testing here is OUR code (routing, validation, error handling) — not
whether Gemini itself works.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import MenuDescriptionResponse

client = TestClient(app)


def test_health_check():
    """The root route should confirm the API is alive."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("app.routers.menu.generate_description")
def test_generate_success(mock_generate):
    """A valid request returns a 200 with the expected shape."""
    mock_generate.return_value = MenuDescriptionResponse(
        name="Tostones",
        description_es="Descripción de prueba en español.",
        description_en="Test description in English.",
    )

    response = client.post(
        "/menu/generate",
        json={
            "name": "Tostones",
            "ingredients": "plátano verde, sal, aceite",
            "tone": "casual",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Tostones"
    assert "description_es" in data
    assert "description_en" in data


def test_generate_missing_name():
    """An empty dish name should fail validation before hitting the AI."""
    response = client.post(
        "/menu/generate",
        json={"name": "", "ingredients": "algo"},
    )
    assert response.status_code == 422  # FastAPI's validation error code


@patch("app.routers.menu.generate_description")
def test_generate_connection_error(mock_generate):
    """If the AI provider is unreachable, we return 503."""
    mock_generate.side_effect = ConnectionError("Simulated network failure")

    response = client.post(
        "/menu/generate",
        json={"name": "Tostones", "ingredients": "plátano verde"},
    )

    assert response.status_code == 503


@patch("app.routers.menu.generate_description")
def test_generate_bad_format_error(mock_generate):
    """If the AI returns malformed JSON, we return 502."""
    mock_generate.side_effect = ValueError("Simulated bad JSON from model")

    response = client.post(
        "/menu/generate",
        json={"name": "Tostones", "ingredients": "plátano verde"},
    )

    assert response.status_code == 502
