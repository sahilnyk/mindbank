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


@pytest.fixture
def neutral_text():
    return "Your task is complete. The deadline is March 15th."


def test_personality_engine_has_strategies(engine):
    assert "calm_mentor" in engine.strategies
    assert "witty_friend" in engine.strategies
    assert "therapist" in engine.strategies


def test_calm_mentor_strategy_exists(engine):
    strategy = engine.strategies["calm_mentor"]
    assert isinstance(strategy, CalmMentorStrategy)


def test_witty_friend_strategy_exists(engine):
    strategy = engine.strategies["witty_friend"]
    assert isinstance(strategy, WittyFriendStrategy)


def test_therapist_strategy_exists(engine):
    strategy = engine.strategies["therapist"]
    assert isinstance(strategy, TherapistStrategy)


def test_all_strategies_inherit_from_base(engine):
    for personality, strategy in engine.strategies.items():
        assert isinstance(strategy, RewriteStrategy)


def test_calm_mentor_rewrite_changes_text(engine, neutral_text):
    result = engine.rewrite(neutral_text, "calm_mentor")
    assert result != neutral_text
    assert len(result) > 0


def test_witty_friend_rewrite_changes_text(engine, neutral_text):
    result = engine.rewrite(neutral_text, "witty_friend")
    assert result != neutral_text
    assert len(result) > 0


def test_therapist_rewrite_changes_text(engine, neutral_text):
    result = engine.rewrite(neutral_text, "therapist")
    assert result != neutral_text
    assert len(result) > 0


def test_calm_mentor_adds_thoughtful_language():
    strategy = CalmMentorStrategy()
    text = "You should do this task"
    result = strategy.rewrite(text)
    
    assert "you might consider" in result.lower() or "you should" not in result.lower()


def test_witty_friend_adds_casual_tone():
    strategy = WittyFriendStrategy()
    text = "Hello, this is great"
    result = strategy.rewrite(text)
    
    assert "Hey there" in result or "😄" in result or "👍" in result


def test_therapist_adds_validation():
    strategy = TherapistStrategy()
    text = "I'm feeling stressed"
    result = strategy.rewrite(text)
    
    validations = ["I hear you", "That makes sense", "I understand", "valid"]
    has_validation = any(val in result for val in validations)
    assert has_validation


def test_therapist_adds_questions():
    strategy = TherapistStrategy()
    text = "I'm feeling stressed"
    result = strategy.rewrite(text)
    
    assert "?" in result


def test_engine_raises_error_for_unknown_personality(engine, neutral_text):
    with pytest.raises(ValueError) as exc_info:
        engine.rewrite(neutral_text, "unknown_personality")
    
    assert "Unknown personality" in str(exc_info.value)


def test_engine_preserves_critical_dates(engine):
    text = "The meeting is on March 15th at 3:00 PM"
    result = engine.rewrite(text, "calm_mentor")
    
    assert "March" in result or "march" in result
    assert "15" in result


def test_engine_preserves_critical_names(engine):
    text = "Sarah will handle this task"
    result = engine.rewrite(text, "witty_friend")
    
    assert "Sarah" in result or "sarah" in result


def test_extract_critical_tokens_finds_dates(engine):
    text = "Deadline is March 15th and also 12/25/2024"
    tokens = engine._extract_critical_tokens(text)
    
    assert len(tokens) >= 2
    date_found = any("March" in token or "12/25" in token for token in tokens)
    assert date_found


def test_extract_critical_tokens_finds_times(engine):
    text = "Meeting at 3:00 PM and 10:30 AM"
    tokens = engine._extract_critical_tokens(text)
    
    assert len(tokens) >= 2


def test_extract_critical_tokens_finds_names(engine):
    text = "John Smith and Sarah Johnson are attending"
    tokens = engine._extract_critical_tokens(text)
    
    assert len(tokens) >= 2
    name_found = any("John" in token or "Sarah" in token for token in tokens)
    assert name_found


def test_preserve_critical_tokens_appends_missing(engine):
    rewritten = "This is the rewritten text"
    critical_tokens = ["March 15th", "Sarah"]
    
    result = engine._preserve_critical_tokens(rewritten, critical_tokens)
    
    assert "Important:" in result or "March 15th" in result.lower()


def test_different_personalities_produce_different_outputs(engine):
    text = "Your task is complete"
    
    calm = engine.rewrite(text, "calm_mentor")
    witty = engine.rewrite(text, "witty_friend")
    therapist = engine.rewrite(text, "therapist")
    
    assert calm != witty
    assert witty != therapist
    assert calm != therapist
