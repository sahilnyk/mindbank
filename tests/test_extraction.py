import json
import pytest
from pathlib import Path
from backend.app.extraction import Extractor
from backend.app.validators import validate_memory, ValidationError


@pytest.fixture
def sample_messages():
    messages_path = Path(__file__).parent.parent / "examples" / "30_messages.json"
    with open(messages_path, "r") as f:
        return json.load(f)


@pytest.fixture
def extractor():
    return Extractor()


def test_extractor_loads_spacy_model(extractor):
    assert extractor.nlp is not None
    assert "core_web_sm" in extractor.nlp.meta["name"]


def test_extract_returns_dict(extractor, sample_messages):
    result = extractor.extract(sample_messages)
    assert isinstance(result, dict)


def test_extract_has_required_keys(extractor, sample_messages):
    result = extractor.extract(sample_messages)
    required_keys = ["user_id", "generated_at", "preferences", "emotional_patterns", "facts", "raw_extractions"]
    for key in required_keys:
        assert key in result


def test_extract_validates_against_schema(extractor, sample_messages):
    result = extractor.extract(sample_messages)
    validate_memory(result)


def test_extract_finds_preferences(extractor, sample_messages):
    result = extractor.extract(sample_messages)
    assert len(result["preferences"]) > 0
    
    if result["preferences"]:
        pref = result["preferences"][0]
        assert "category" in pref
        assert "value" in pref
        assert "confidence" in pref
        assert "source_messages" in pref
        assert 0 <= pref["confidence"] <= 1


def test_extract_finds_emotional_patterns(extractor, sample_messages):
    result = extractor.extract(sample_messages)
    assert len(result["emotional_patterns"]) > 0


def test_extract_finds_facts(extractor, sample_messages):
    result = extractor.extract(sample_messages)
    assert len(result["facts"]) > 0


def test_extract_source_messages_are_valid(extractor, sample_messages):
    result = extractor.extract(sample_messages)
    max_index = len(sample_messages) - 1
    
    for pref in result["preferences"]:
        for idx in pref["source_messages"]:
            assert 0 <= idx <= max_index


def test_validate_memory_rejects_invalid_data():
    invalid_memory = {"user_id": "test"}
    
    with pytest.raises(ValidationError):
        validate_memory(invalid_memory)


def test_extract_deduplicates_entries(extractor):
    messages = [
        {"index": 0, "role": "user", "content": "I'm vegetarian"},
        {"index": 1, "role": "user", "content": "I'm vegetarian btw"},
        {"index": 2, "role": "user", "content": "Did I mention I'm vegetarian?"},
    ]
    
    result = extractor.extract(messages)
    vegetarian_prefs = [p for p in result["preferences"] if "vegetarian" in p["value"].lower()]
    assert len(vegetarian_prefs) == 1