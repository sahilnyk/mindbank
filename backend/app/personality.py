import re
from abc import ABC, abstractmethod
from typing import Dict


class RewriteStrategy(ABC):
    
    @abstractmethod
    def rewrite(self, neutral_text: str) -> str:
        pass


class CalmMentorStrategy(RewriteStrategy):
    
    def rewrite(self, neutral_text: str) -> str:
        templates = [
            "Take a moment to consider this: {}",
            "Here's a thoughtful perspective: {}",
            "Let me share something with you: {}",
            "I'd encourage you to reflect on this: {}"
        ]
        
        text = neutral_text.lower()
        text = text.replace("you should", "you might consider")
        text = text.replace("you must", "it would be wise to")
        text = text.replace("do this", "explore this approach")
        
        import random
        template = random.choice(templates)
        return template.format(text.capitalize())


class WittyFriendStrategy(RewriteStrategy):
    
    def rewrite(self, neutral_text: str) -> str:
        emojis = ["😄", "👍", "✨", "🎯", "💡"]
        
        text = neutral_text
        text = text.replace("Hello", "Hey there")
        text = text.replace("Okay", "Cool")
        text = text.replace("Yes", "Yep")
        text = text.replace("No", "Nah")
        
        import random
        emoji = random.choice(emojis)
        
        casual_endings = [
            f" {emoji}",
            f" Pretty neat, right? {emoji}",
            f" Just saying! {emoji}",
            f" {emoji} Hope that helps!"
        ]
        
        return text + random.choice(casual_endings)


class TherapistStrategy(RewriteStrategy):
    
    def rewrite(self, neutral_text: str) -> str:
        validations = [
            "I hear you. ",
            "That makes sense. ",
            "I understand. ",
            "It's completely valid to feel this way. "
        ]
        
        questions = [
            " How does that sit with you?",
            " What feelings does that bring up?",
            " How are you processing that?",
            " What would support you right now?"
        ]
        
        import random
        validation = random.choice(validations)
        question = random.choice(questions)
        
        return validation + neutral_text + question


class PersonalityEngine:
    
    def __init__(self):
        self.strategies: Dict[str, RewriteStrategy] = {
            "calm_mentor": CalmMentorStrategy(),
            "witty_friend": WittyFriendStrategy(),
            "therapist": TherapistStrategy()
        }
    
    def rewrite(self, neutral_text: str, personality: str) -> str:
        if personality not in self.strategies:
            raise ValueError(f"Unknown personality: {personality}")
        
        strategy = self.strategies[personality]
        rewritten = strategy.rewrite(neutral_text)
        
        critical_tokens = self._extract_critical_tokens(neutral_text)
        rewritten = self._preserve_critical_tokens(rewritten, critical_tokens)
        
        return rewritten
    
    def _extract_critical_tokens(self, text: str) -> list:
        critical = []
        
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?\b'
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        critical.extend(dates)
        
        time_pattern = r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b'
        times = re.findall(time_pattern, text)
        critical.extend(times)
        
        name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        names = re.findall(name_pattern, text)
        critical.extend(names)
        
        return critical
    
    def _preserve_critical_tokens(self, rewritten: str, critical_tokens: list) -> str:
        missing_tokens = []
        
        for token in critical_tokens:
            if token.lower() not in rewritten.lower():
                missing_tokens.append(token)
        
        if missing_tokens:
            rewritten += f" (Important: {', '.join(missing_tokens)})"
        
        return rewritten