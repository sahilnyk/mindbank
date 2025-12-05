import pytest
from backend.app.personality import (
    PersonalityEngine,
    CalmMentorStrategy,
    WittyFriendStrategy,
    TherapistStrategy,
    RewriteStrategy
)


@pytest.fixture
def engine():
    return PersonalityEngine()


def test_personality_engine_has_personalities(engine):
    """Test engine has personalities dict"""
    assert hasattr(engine, 'personalities')
    assert "calm_mentor" in engine.personalities
    assert "witty_friend" in engine.personalities
    assert "therapist" in engine.personalities


def test_calm_mentor_strategy_exists():
    """Test CalmMentorStrategy class exists"""
    strategy = CalmMentorStrategy()
    assert isinstance(strategy, RewriteStrategy)


def test_witty_friend_strategy_exists():
    """Test WittyFriendStrategy class exists"""
    strategy = WittyFriendStrategy()
    assert isinstance(strategy, RewriteStrategy)


def test_therapist_strategy_exists():
    """Test TherapistStrategy class exists"""
    strategy = TherapistStrategy()
    assert isinstance(strategy, RewriteStrategy)


def test_all_strategies_inherit_from_base():
    """Test all strategies inherit from RewriteStrategy"""
    strategies = [CalmMentorStrategy(), WittyFriendStrategy(), TherapistStrategy()]
    for strategy in strategies:
        assert isinstance(strategy, RewriteStrategy)
        assert hasattr(strategy, 'rewrite')


def test_calm_mentor_rewrite_changes_text():
    strategy = CalmMentorStrategy()
    text = "You should do this"
    result = strategy.rewrite(text)
    assert result != text
    assert len(result) > len(text)


def test_witty_friend_rewrite_changes_text():
    strategy = WittyFriendStrategy()
    text = "You should do this"
    result = strategy.rewrite(text)
    assert result != text
    assert len(result) > len(text)


def test_therapist_rewrite_changes_text():
    strategy = TherapistStrategy()
    text = "You should do this"
    result = strategy.rewrite(text)
    assert result != text
    assert len(result) > len(text)


def test_calm_mentor_adds_framing():
    """Test calm mentor adds wisdom framing"""
    strategy = CalmMentorStrategy()
    text = "Take breaks to avoid burnout"
    result = strategy.rewrite(text)
    
    assert not result.startswith(text)
    assert not result.endswith(text)


def test_witty_friend_adds_casual_tone():
    """Test witty friend adds casual language"""
    strategy = WittyFriendStrategy()
    text = "Hello, this is great"
    result = strategy.rewrite(text)
    casual_markers = ["Yo", "Alright", "Here's", "Okay", "Not gonna", "💪", "🎯", "😄", "✨", "🚀", "💡"]
    assert any(marker in result for marker in casual_markers)


def test_therapist_adds_validation():
    strategy = TherapistStrategy()
    text = "You should consider your options"
    result = strategy.rewrite(text)
    
    validation_phrases = ["hear", "valid", "thank you", "appreciate", "makes sense"]
    assert any(phrase in result.lower() for phrase in validation_phrases)


def test_therapist_adds_questions():
    strategy = TherapistStrategy()
    text = "You should consider your options"
    result = strategy.rewrite(text)
    
    assert "?" in result


def test_engine_raises_error_for_unknown_personality(engine):
    with pytest.raises(ValueError):
        engine.rewrite("Some text", "unknown_personality")


def test_engine_preserves_content():
    """Test that personality transformation preserves core content"""
    engine = PersonalityEngine()
    text = "Berlin is a great city for remote work"
    
    results = []
    for personality in ["calm_mentor", "witty_friend", "therapist"]:
        result = engine.rewrite(text, personality)
        results.append(result)
        assert "Berlin" in result or "berlin" in result


def test_different_personalities_produce_different_outputs():
    engine = PersonalityEngine()
    text = "You should take a break"
    
    calm = engine.rewrite(text, "calm_mentor")
    witty = engine.rewrite(text, "witty_friend")
    therapist = engine.rewrite(text, "therapist")
    
    assert calm != witty
    assert witty != therapist
    assert calm != therapist


def test_generate_memory_aware_response_work_question(engine):
    """Test memory-aware response for work questions"""
    memory = {
        "preferences": [
            {"category": "work_style", "value": "works late", "confidence": 0.85}
        ],
        "emotional_patterns": [],
        "facts": []
    }
    
    response = engine.generate_memory_aware_response(memory, "Should I work tonight?")
    assert len(response) > 0
    assert isinstance(response, str)


def test_generate_memory_aware_response_food_question(engine):
    """Test memory-aware response for food questions"""
    memory = {
        "preferences": [
            {"category": "food", "value": "vegetarian", "confidence": 0.95}
        ],
        "emotional_patterns": [],
        "facts": [
            {"fact_type": "health", "value": "allergic to peanuts", "confidence": 0.95}
        ]
    }
    
    response = engine.generate_memory_aware_response(memory, "What should I eat?")
    assert len(response) > 0
    assert "vegetarian" in response.lower() or "plant" in response.lower()


def test_generate_memory_aware_response_generic_question(engine):
    """Test response for questions without specific memory context"""
    memory = {
        "preferences": [],
        "emotional_patterns": [],
        "facts": []
    }
    
    response = engine.generate_memory_aware_response(memory, "How do I learn programming?")
    assert len(response) > 0
    assert isinstance(response, str)
