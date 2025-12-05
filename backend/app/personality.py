import re
from abc import ABC, abstractmethod
from typing import Dict, Any
import random


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
        
        validation = random.choice(validations)
        question = random.choice(questions)
        
        return validation + neutral_text + question


class PersonalityEngine:
    def __init__(self):
        self.personalities = {
            "calm_mentor": {
                "tone": "wise, patient, encouraging",
                "phrases": [
                    "I understand that", "It's natural to", "Consider this perspective",
                    "Take your time with", "You're making progress", "Let me guide you through"
                ]
            },
            "witty_friend": {
                "tone": "casual, humorous, relatable",
                "phrases": [
                    "Haha, I feel you!", "That's hilarious!", "No joke though",
                    "Real talk:", "Honestly though", "You know what's funny?"
                ]
            },
            "therapist": {
                "tone": "empathetic, validating, reflective",
                "phrases": [
                    "I hear you saying", "That must feel", "It sounds like",
                    "How does that make you feel?", "Let's explore that",
                    "Your feelings are valid"
                ]
            }
        }
    
    def generate_memory_aware_response(self, memory: Dict[str, Any], user_message: str) -> str:
        preferences = memory.get("preferences", [])
        emotional_patterns = memory.get("emotional_patterns", [])
        facts = memory.get("facts", [])
        
        context_parts = []
        
        if preferences:
            pref_values = []
            for pref in preferences[:3]:
                if isinstance(pref, dict):
                    pref_values.append(pref.get("value", ""))
                else:
                    pref_values.append(str(pref))
            
            if pref_values:
                pref_text = ", ".join(pref_values)
                context_parts.append(f"I remember you prefer {pref_text}")
        
        if emotional_patterns:
            negative_emotions = ["stress", "anxious", "overwhelmed", "frustrated", "overthinking"]
            positive_emotions = ["appreciation", "grateful", "thankful", "happy"]
            
            patterns = [p.get("pattern", "") if isinstance(p, dict) else str(p) for p in emotional_patterns]
            
            if any(emotion in patterns for emotion in negative_emotions):
                context_parts.append("I sense you might be feeling a bit overwhelmed lately")
            elif any(emotion in patterns for emotion in positive_emotions):
                context_parts.append("It's great to see your positive energy")
        
        if facts:
            fact_values = []
            for fact in facts[:2]:
                if isinstance(fact, dict):
                    fact_type = fact.get("fact_type", "")
                    fact_value = fact.get("value", "")
                    
                    if fact_type == "location" and fact_value:
                        fact_values.append(f"you're in {fact_value}")
                    elif fact_type == "time" and fact_value:
                        fact_values.append(f"it's {fact_value}")
            
            if fact_values:
                context_parts.append(f"I know {' and '.join(fact_values)}")
        
        if context_parts:
            base = f"{random.choice(context_parts)}. "
        else:
            base = ""
        
        message_lower = user_message.lower()
        
        if "stress" in message_lower or "overwhelm" in message_lower:
            base += "It's important to take things one step at a time. Consider breaking down your tasks into smaller, manageable pieces."
        elif "help" in message_lower:
            base += "I'm here to support you. Let's work through this together and find the best approach."
        elif "work" in message_lower:
            base += "Finding the right work-life balance is key. Make sure you're taking care of yourself too."
        else:
            base += "Every challenge is an opportunity for growth. Stay focused on your goals."
        
        return base
    
    def rewrite(self, text: str, personality: str) -> str:
        if personality not in self.personalities:
            raise ValueError(f"Unknown personality: {personality}")
        
        profile = self.personalities[personality]
        prefix = random.choice(profile["phrases"])
        
        if personality == "calm_mentor":
            return f"{prefix}. {text} Remember, growth takes time and patience."
        elif personality == "witty_friend":
            return f"{prefix} {text} But hey, you got this! 💪"
        elif personality == "therapist":
            return f"{prefix}. {text} How are you feeling about this?"
        
        return text