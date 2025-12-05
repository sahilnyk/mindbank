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
        
        message_lower = user_message.lower()
        
        context_parts = []
        base_response = ""
        
        if "stress" in message_lower or "overwhelm" in message_lower or "anxious" in message_lower:
            if emotional_patterns:
                negative_emotions = ["stress", "anxious", "overwhelmed", "frustrated", "overthinking"]
                patterns = [p.get("pattern", "") if isinstance(p, dict) else str(p) for p in emotional_patterns]
                
                if any(emotion in patterns for emotion in negative_emotions):
                    context_parts.append("I notice you've been dealing with stress lately")
            
            base_response = "It's important to take things one step at a time. Consider breaking down your tasks into smaller, manageable pieces. Taking short breaks can also help reset your mind."
        
        elif "work" in message_lower or "project" in message_lower or "deadline" in message_lower:
            if preferences:
                work_prefs = []
                for pref in preferences:
                    if isinstance(pref, dict):
                        value = pref.get("value", "")
                        category = pref.get("category", "")
                        if category in ["work", "communication", "time"]:
                            work_prefs.append(value)
                
                if work_prefs:
                    context_parts.append(f"I remember you prefer {', '.join(work_prefs[:2])}")
            
            base_response = "Finding the right work-life balance is key. Structure your tasks during your most productive hours and don't forget to take care of yourself."
        
        elif "learn" in message_lower or "study" in message_lower or "course" in message_lower:
            base_response = "Learning new skills is always valuable. Start with what aligns with your goals and interests. Take it step by step, and practice consistently."
        
        elif "food" in message_lower or "eat" in message_lower or "cook" in message_lower or "dinner" in message_lower:
            if preferences:
                food_prefs = []
                for pref in preferences:
                    if isinstance(pref, dict):
                        value = pref.get("value", "")
                        category = pref.get("category", "")
                        if category == "food":
                            food_prefs.append(value)
                
                if food_prefs:
                    context_parts.append(f"Given that you're {', '.join(food_prefs)}")
            
            if facts:
                allergies = []
                for fact in facts:
                    if isinstance(fact, dict):
                        fact_type = fact.get("fact_type", "")
                        value = fact.get("value", "")
                        if "allerg" in value.lower():
                            allergies.append(value)
                
                if allergies:
                    context_parts.append(f"and avoiding {', '.join(allergies)}")
            
            base_response = "Try to maintain a balanced diet with foods you enjoy. Planning meals ahead can reduce daily stress."
        
        elif "meeting" in message_lower or "call" in message_lower or "communicate" in message_lower:
            if preferences:
                comm_prefs = []
                for pref in preferences:
                    if isinstance(pref, dict):
                        value = pref.get("value", "")
                        category = pref.get("category", "")
                        if category == "communication":
                            comm_prefs.append(value)
                
                if comm_prefs:
                    context_parts.append(f"I know you prefer {', '.join(comm_prefs)}")
            
            base_response = "Choose communication methods that work best for you. It's okay to set boundaries around your preferred style."
        
        elif "pet" in message_lower or "cat" in message_lower or "dog" in message_lower:
            if facts:
                pets = []
                for fact in facts:
                    if isinstance(fact, dict):
                        value = fact.get("value", "")
                        if any(word in value.lower() for word in ["cat", "dog", "pet", "luna"]):
                            pets.append(value)
                
                if pets:
                    context_parts.append(f"I remember you have {pets[0]}")
            
            base_response = "Pets can be wonderful companions but also need attention. Try setting specific times for play and work to maintain balance."
        
        elif "weekend" in message_lower or "activity" in message_lower or "do" in message_lower:
            if facts:
                for fact in facts:
                    if isinstance(fact, dict):
                        fact_type = fact.get("fact_type", "")
                        value = fact.get("value", "")
                        if fact_type == "location":
                            context_parts.append(f"Since you're in {value}")
                            break
            
            base_response = "Explore activities that interest you. Balance relaxation with things that energize you."
        
        else:
            base_response = "That's a great question. Consider what aligns with your goals and values. Take your time to explore the options available to you."
        
        if context_parts:
            return f"{', '.join(context_parts)}. {base_response}"
        else:
            return base_response
    
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