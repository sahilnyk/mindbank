import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_messages():
    return [
        {"index": 0, "role": "user", "content": "I'm vegetarian"},
        {"index": 1, "role": "user", "content": "I live in Berlin"},
        {"index": 2, "role": "user", "content": "Feeling stressed"}
    ]


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "llm_available" in data
    assert "components" in data


def test_extract_deterministic(client, sample_messages):
    response = client.post("/extract", json={
        "messages": sample_messages,
        "use_llm": False
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "memory" in data
    assert data["method"] == "deterministic"
    
    memory = data["memory"]
    assert "user_id" in memory
    assert "preferences" in memory
    assert "emotional_patterns" in memory
    assert "facts" in memory


def test_extract_with_invalid_messages(client):
    response = client.post("/extract", json={
        "messages": [{"invalid": "data"}],
        "use_llm": False
    })
    
    assert response.status_code == 422


def test_rewrite_deterministic_calm_mentor(client):
    response = client.post("/rewrite", json={
        "text": "Your task is complete",
        "personality": "calm_mentor",
        "use_llm": False
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "rewritten" in data
    assert data["personality"] == "calm_mentor"
    assert data["method"] == "deterministic"
    assert data["rewritten"] != data["original"]


def test_rewrite_deterministic_witty_friend(client):
    response = client.post("/rewrite", json={
        "text": "That's great",
        "personality": "witty_friend",
        "use_llm": False
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["personality"] == "witty_friend"


def test_rewrite_deterministic_therapist(client):
    response = client.post("/rewrite", json={
        "text": "I'm feeling down",
        "personality": "therapist",
        "use_llm": False
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["personality"] == "therapist"


def test_rewrite_invalid_personality(client):
    response = client.post("/rewrite", json={
        "text": "Hello",
        "personality": "invalid_personality",
        "use_llm": False
    })
    
    assert response.status_code == 400
    assert "Invalid personality" in response.json()["detail"]


def test_extract_with_llm_fallback(client, sample_messages):
    response = client.post("/extract", json={
        "messages": sample_messages,
        "use_llm": True
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "method" in data


def test_rewrite_with_llm_fallback(client):
    response = client.post("/rewrite", json={
        "text": "Your task is complete",
        "personality": "calm_mentor",
        "use_llm": True
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "method" in data