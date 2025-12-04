import pytest
import os
from backend.app.llm_client import LLMClient, NoLLMAvailable


@pytest.fixture
def no_api_key_client(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    return LLMClient(api_key=None)


@pytest.fixture
def mock_api_key_client():
    return LLMClient(api_key="test-key-12345")


@pytest.fixture
def sample_messages():
    return [
        {"index": 0, "role": "user", "content": "I'm vegetarian"},
        {"index": 1, "role": "user", "content": "I live in Berlin"},
        {"index": 2, "role": "user", "content": "Feeling stressed today"}
    ]


def test_client_without_api_key_not_available(no_api_key_client):
    assert not no_api_key_client.is_available()


def test_client_with_placeholder_key_not_available():
    client = LLMClient(api_key="your-openai-api-key-here")
    assert not client.is_available()


def test_client_initialization_without_openai_package(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
    
    import sys
    monkeypatch.setitem(sys.modules, 'openai', None)
    
    with pytest.raises(NoLLMAvailable):
        LLMClient()


def test_extract_memories_raises_when_not_available(no_api_key_client, sample_messages):
    with pytest.raises(NoLLMAvailable):
        no_api_key_client.extract_memories(sample_messages)


def test_rewrite_raises_when_not_available(no_api_key_client):
    with pytest.raises(NoLLMAvailable):
        no_api_key_client.rewrite_with_personality("Hello", "calm_mentor")


def test_rewrite_raises_for_unknown_personality(mock_api_key_client):
    with pytest.raises(ValueError) as exc_info:
        mock_api_key_client.rewrite_with_personality("Hello", "unknown")
    
    assert "Unknown personality" in str(exc_info.value)


def test_close_clears_client(mock_api_key_client):
    mock_api_key_client.close()
    assert not mock_api_key_client.is_available()


def test_client_with_real_key_is_available():
    real_key = os.getenv("OPENAI_API_KEY")
    if real_key and real_key != "your-openai-api-key-here":
        client = LLMClient()
        assert client.is_available()
    else:
        pytest.skip("No real OpenAI API key available")


def test_extract_memories_with_real_api(sample_messages):
    real_key = os.getenv("OPENAI_API_KEY")
    if not real_key or real_key == "your-openai-api-key-here":
        pytest.skip("No real OpenAI API key available")
    
    client = LLMClient()
    if not client.is_available():
        pytest.skip("LLM not available")
    
    try:
        result = client.extract_memories(sample_messages)
        
        assert "user_id" in result
        assert "generated_at" in result
        assert "preferences" in result
        assert "emotional_patterns" in result
        assert "facts" in result
        
    except NoLLMAvailable:
        pytest.skip("LLM call failed")


def test_rewrite_with_real_api():
    real_key = os.getenv("OPENAI_API_KEY")
    if not real_key or real_key == "your-openai-api-key-here":
        pytest.skip("No real OpenAI API key available")
    
    client = LLMClient()
    if not client.is_available():
        pytest.skip("LLM not available")
    
    try:
        text = "Your task is complete"
        result = client.rewrite_with_personality(text, "calm_mentor")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert result != text
        
    except NoLLMAvailable:
        pytest.skip("LLM call failed")