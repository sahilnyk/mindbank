from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "llm_available" in data
    assert "components" in data


def test_extract_deterministic(client):
    payload = {
        "messages": [
            {"index": 0, "role": "user", "content": "I'm vegetarian"},
            {"index": 1, "role": "user", "content": "I live in Berlin"}
        ],
        "use_llm": False
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "memory" in data
    assert data["method"] == "deterministic"


def test_extract_with_invalid_messages(client):
    payload = {
        "messages": [],
        "use_llm": False
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_rewrite_deterministic_calm_mentor(client):
    payload = {
        "text": "You should take a break",
        "personality": "calm_mentor",
        "use_llm": False
    }
    response = client.post("/rewrite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["personality"] == "calm_mentor"
    assert data["method"] == "deterministic"


def test_rewrite_deterministic_witty_friend(client):
    payload = {
        "text": "You should take a break",
        "personality": "witty_friend",
        "use_llm": False
    }
    response = client.post("/rewrite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["personality"] == "witty_friend"


def test_rewrite_deterministic_therapist(client):
    payload = {
        "text": "You should take a break",
        "personality": "therapist",
        "use_llm": False
    }
    response = client.post("/rewrite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["personality"] == "therapist"


def test_rewrite_invalid_personality(client):
    payload = {
        "text": "You should take a break",
        "personality": "invalid_personality",
        "use_llm": False
    }
    response = client.post("/rewrite", json=payload)
    assert response.status_code == 400


def test_extract_with_llm_fallback(client):
    payload = {
        "messages": [
            {"index": 0, "role": "user", "content": "I'm vegetarian"}
        ],
        "use_llm": True
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["method"] in ["llm", "deterministic"]


def test_rewrite_with_llm_fallback(client):
    payload = {
        "text": "You should take a break",
        "personality": "calm_mentor",
        "use_llm": True
    }
    response = client.post("/rewrite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["method"] in ["llm", "deterministic"]