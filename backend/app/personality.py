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
            "Let me share a perspective with you. {}",
            "I've been thinking about this. {}",
            "Here's what I've observed: {}",
            "Consider this approach: {}",
            "From my experience, {}",
            "Let's think through this together. {}"
        ]
        
        endings = [
            " Take your time with this decision.",
            " Trust the process - you're on the right path.",
            " Small steps lead to meaningful progress.",
            " Be patient with yourself as you navigate this.",
            " Every challenge teaches us something valuable.",
            " You have the wisdom within you to figure this out."
        ]
        
        template = random.choice(templates)
        ending = random.choice(endings)
        
        return template.format(neutral_text) + ending


class WittyFriendStrategy(RewriteStrategy):
    
    def rewrite(self, neutral_text: str) -> str:
        intros = [
            "Yo, listen up! ",
            "Alright, real talk - ",
            "Here's the deal: ",
            "Okay so check it out - ",
            "Not gonna lie, ",
            "Here's my two cents: "
        ]
        
        endings = [
            " 🎯 You got this!",
            " 💪 Trust me on this one!",
            " 😄 But hey, that's just me!",
            " ✨ Make it happen!",
            " 🚀 Go crush it!",
            " 💡 Pretty solid advice if you ask me!"
        ]
        
        intro = random.choice(intros)
        ending = random.choice(endings)
        
        casual_text = neutral_text.replace("you should", "you could totally")
        casual_text = casual_text.replace("it is important", "it's super important")
        casual_text = casual_text.replace("consider", "think about")
        
        return intro + casual_text + ending


class TherapistStrategy(RewriteStrategy):
    
    def rewrite(self, neutral_text: str) -> str:
        validations = [
            "I really hear what you're saying. ",
            "Your feelings about this are completely valid. ",
            "Thank you for sharing this with me. ",
            "I appreciate you opening up about this. ",
            "It sounds like you're navigating something important. ",
            "What you're experiencing makes complete sense. "
        ]
        
        questions = [
            " How does this feel for you right now?",
            " What emotions come up when you think about this?",
            " How are you taking care of yourself through this?",
            " What would feel most supportive to you?",
            " How can you honor what you need in this moment?",
            " What does your inner voice tell you about this?"
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
        
        if "stress" in message_lower or "overwhelm" in message_lower or "anxious" in message_lower or "pressure" in message_lower:
            responses = [
                "Break things down into smaller, manageable steps. Focus on what you can control right now, and let go of what you can't. Taking short breaks throughout your day can help reset your nervous system.",
                "When feeling overwhelmed, pause and take three deep breaths. Write down everything on your mind, then prioritize just the top three items. You don't have to tackle everything at once.",
                "Stress often comes from trying to control too much. Identify what's truly urgent versus what can wait. Give yourself permission to not be perfect - progress matters more than perfection."
            ]
            
            if emotional_patterns:
                negative_emotions = ["stress", "anxious", "overwhelmed", "frustrated", "overthinking", "tired"]
                patterns = [p.get("pattern", "") if isinstance(p, dict) else str(p) for p in emotional_patterns]
                
                if any(emotion in patterns for emotion in negative_emotions):
                    context_parts.append("I've noticed you've been carrying a lot lately")
            
            base_response = random.choice(responses)
        
        elif "work" in message_lower or "project" in message_lower or "deadline" in message_lower or "job" in message_lower:
            responses = [
                "Structure your work around your natural energy peaks. Block out focused time for deep work, and use lower-energy periods for meetings or admin tasks. Protect your productive hours fiercely.",
                "Set clear boundaries between work and personal time. Your brain needs recovery periods to perform at its best. Consider time-blocking your calendar to create structure without rigidity.",
                "Quality work comes from sustainable routines, not constant hustle. Build in buffer time for unexpected issues, and communicate realistic timelines. It's better to under-promise and over-deliver."
            ]
            
            if preferences:
                work_prefs = []
                for pref in preferences:
                    if isinstance(pref, dict):
                        value = pref.get("value", "")
                        category = pref.get("category", "")
                        if category in ["work_style", "communication"]:
                            work_prefs.append(value)
                
                if work_prefs:
                    context_parts.append(f"Given that you {', '.join(work_prefs[:2])}")
            
            base_response = random.choice(responses)
        
        elif "learn" in message_lower or "study" in message_lower or "course" in message_lower or "skill" in message_lower:
            responses = [
                "Choose one skill and commit to 30 days of consistent practice. Even 20 minutes daily builds momentum. Focus on application, not just consumption - build projects while you learn.",
                "Start with the fundamentals and resist jumping ahead. Master the basics through repetition, then layer on complexity. Learning is a marathon, not a sprint.",
                "Find a learning style that matches your strengths. Some people learn by doing, others by teaching. Experiment with different methods until you find what clicks for you."
            ]
            base_response = random.choice(responses)
        
        elif "food" in message_lower or "eat" in message_lower or "cook" in message_lower or "dinner" in message_lower or "meal" in message_lower:
            responses = [
                "Plan your meals at the start of the week to reduce daily decision fatigue. Batch cook basics like grains and proteins that you can mix and match. Keep it simple - nutrition doesn't have to be complicated.",
                "Listen to your body's hunger cues rather than eating by the clock. Choose whole foods that make you feel energized, not sluggish. Meal prep can be as simple as chopping vegetables in advance.",
                "Build meals around foods you genuinely enjoy - sustainable eating isn't about restriction. Having go-to simple recipes removes the stress of daily cooking decisions."
            ]
            
            if preferences:
                food_prefs = []
                for pref in preferences:
                    if isinstance(pref, dict):
                        value = pref.get("value", "")
                        category = pref.get("category", "")
                        if category == "food":
                            food_prefs.append(value)
                
                if food_prefs:
                    context_parts.append(f"Since you're {', '.join(food_prefs)}")
            
            if facts:
                allergies = []
                for fact in facts:
                    if isinstance(fact, dict):
                        value = fact.get("value", "")
                        if "allerg" in value.lower():
                            allergies.append(value)
                
                if allergies:
                    context_parts.append(f"and need to avoid {', '.join(allergies)}")
            
            base_response = random.choice(responses)
        
        elif "meeting" in message_lower or "call" in message_lower or "communicate" in message_lower or "talk" in message_lower:
            responses = [
                "Set clear agendas before meetings and stick to them. If it can be an email, make it an email. Your time and focus are valuable resources - protect them accordingly.",
                "Communicate your preferred working style upfront to set expectations. Async communication often leads to more thoughtful responses. Don't feel guilty about declining meetings that don't need you.",
                "Block out 'no meeting' time on your calendar for focused work. When meetings are necessary, keep them short and action-oriented. End each meeting with clear next steps and owners."
            ]
            
            if preferences:
                comm_prefs = []
                for pref in preferences:
                    if isinstance(pref, dict):
                        value = pref.get("value", "")
                        category = pref.get("category", "")
                        if category == "communication":
                            comm_prefs.append(value)
                
                if comm_prefs:
                    context_parts.append(f"I know you work best with {', '.join(comm_prefs)}")
            
            base_response = random.choice(responses)
        
        elif "pet" in message_lower or "cat" in message_lower or "dog" in message_lower or "animal" in message_lower:
            responses = [
                "Create a routine for pet care that fits naturally into your day. Pets thrive on consistency, and so do we. Set specific times for play, feeding, and attention so it doesn't feel overwhelming.",
                "Your pet can actually help reduce stress when you build in intentional interaction time. Short play sessions throughout the day can be refreshing breaks that benefit both of you.",
                "Balance is key - your pet needs attention, but you also need focused work time. Create a dedicated space where your pet knows it's quiet time, using positive reinforcement to build the habit."
            ]
            
            if facts:
                pets = []
                for fact in facts:
                    if isinstance(fact, dict):
                        value = fact.get("value", "")
                        if any(word in value.lower() for word in ["cat", "dog", "pet", "luna"]):
                            pets.append(value)
                
                if pets:
                    context_parts.append(f"With {pets[0]}")
            
            base_response = random.choice(responses)
        
        elif "weekend" in message_lower or "activity" in message_lower or "free time" in message_lower or "hobby" in message_lower:
            responses = [
                "Mix energizing activities with restorative ones. Don't overschedule your free time - leave room for spontaneity and rest. The best weekend is one where you feel refreshed, not exhausted.",
                "Try the 'one thing' rule: plan one main activity and leave the rest flexible. This removes pressure while still giving your weekend structure. Sometimes doing nothing is exactly what you need.",
                "Balance social activities with solo recharge time based on what energizes you. Your weekend should refuel you for the week ahead, not drain you further."
            ]
            
            if facts:
                for fact in facts:
                    if isinstance(fact, dict):
                        fact_type = fact.get("fact_type", "")
                        value = fact.get("value", "")
                        if fact_type == "location":
                            context_parts.append(f"Being in {value}")
                            break
            
            base_response = random.choice(responses)
        
        elif "exercise" in message_lower or "fitness" in message_lower or "gym" in message_lower or "workout" in message_lower:
            responses = [
                "Start with movement you actually enjoy - fitness shouldn't feel like punishment. Consistency beats intensity. Even 15 minutes daily creates lasting habits better than sporadic intense sessions.",
                "Build exercise into your existing routine rather than adding it as a separate task. Walk during calls, stretch between work sessions, or bike to errands. Make it convenient and it'll stick.",
                "Focus on how exercise makes you feel rather than how you look. Track energy levels and mood improvements alongside physical metrics. The mental health benefits often show up before physical changes."
            ]
            base_response = random.choice(responses)
        
        elif "sleep" in message_lower or "tired" in message_lower or "rest" in message_lower:
            responses = [
                "Protect your sleep like you'd protect an important meeting. Set a consistent bedtime routine and stick to it, even on weekends. Your phone should charge in another room - your bedroom is for sleep, not scrolling.",
                "Quality sleep is non-negotiable for cognitive performance and emotional regulation. Dim lights an hour before bed, keep your room cool, and avoid caffeine after 2pm. You can't optimize your way out of sleep deprivation.",
                "If you're consistently tired, examine your sleep environment and pre-bed habits. Most sleep issues come from inconsistent schedules and stimulating activities too close to bedtime. Your body craves routine."
            ]
            base_response = random.choice(responses)
        
        elif "friend" in message_lower or "social" in message_lower or "people" in message_lower:
            responses = [
                "Quality relationships require intentional effort but shouldn't feel draining. Protect energy for people who reciprocate care and respect your boundaries. It's okay to let some relationships naturally fade.",
                "Schedule regular check-ins with people who matter, even if brief. Deep friendships aren't built on grand gestures but consistent small connections. A quick message can maintain bonds between bigger hangouts.",
                "Know your social capacity and honor it without guilt. Saying no to some invitations means you can fully show up for the ones you accept. Authentic connection beats surface-level networking every time."
            ]
            
            if preferences:
                for pref in preferences:
                    if isinstance(pref, dict):
                        value = pref.get("value", "")
                        if "introvert" in value or "extrovert" in value:
                            context_parts.append(f"As someone who's {value}")
                            break
            
            base_response = random.choice(responses)
        
        elif "decision" in message_lower or "choice" in message_lower or "should i" in message_lower:
            responses = [
                "Big decisions rarely need to be made instantly. Sleep on it, but set a deadline to avoid analysis paralysis. List pros and cons, then trust your gut - your intuition processes information your conscious mind hasn't caught up to yet.",
                "Consider your decision through three lenses: what makes logical sense, what feels right emotionally, and what aligns with your long-term values. When all three align, you have your answer.",
                "Most decisions are reversible or adjustable. The cost of a wrong decision is often less than the cost of no decision. Make the best choice with current information, then commit and course-correct if needed."
            ]
            base_response = random.choice(responses)
        
        else:
            responses = [
                "Start by clarifying what success looks like for this situation. Break it into smaller questions you can answer more easily. Often, the right path reveals itself when you zoom in on specifics.",
                "There's rarely one perfect answer. Consider what aligns with your values and current life season. What works for others might not work for you, and that's completely fine.",
                "Take a step back and ask yourself what advice you'd give a friend in this situation. We're often clearer about others' situations than our own. That outside perspective can be revealing.",
                "Instead of looking for the 'right' answer, look for the next right step. Forward motion creates clarity that thinking in circles never will. Action beats perfect planning."
            ]
            base_response = random.choice(responses)
        
        if context_parts:
            return f"{', '.join(context_parts)}, {base_response[0].lower()}{base_response[1:]}"
        else:
            return base_response
    
    def rewrite(self, text: str, personality: str) -> str:
        if personality not in self.personalities:
            raise ValueError(f"Unknown personality: {personality}")
        
        if personality == "calm_mentor":
            strategy = CalmMentorStrategy()
        elif personality == "witty_friend":
            strategy = WittyFriendStrategy()
        else:
            strategy = TherapistStrategy()
        
        return strategy.rewrite(text)