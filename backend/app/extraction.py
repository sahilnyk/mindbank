import re
from typing import List, Dict, Any
from datetime import datetime
import spacy


class Extractor:
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        self.patterns = {
            "vegetarian": re.compile(r"\b(vegetarian|vegan|plant-based)\b", re.IGNORECASE),
            "lo-fi": re.compile(r"\b(lo-?fi|lofi)\b", re.IGNORECASE),
            "green tea": re.compile(r"\bgreen tea\b", re.IGNORECASE),
            "async": re.compile(r"\b(async|asynchronous)\b", re.IGNORECASE),
            "hates meetings": re.compile(r"\b(hate|dislike|struggling with).*(meeting|standup)\b", re.IGNORECASE),
            "linux": re.compile(r"\blinux\b", re.IGNORECASE),
            "allergic": re.compile(r"\ballergic to ([a-z]+)\b", re.IGNORECASE),
            "short messages": re.compile(r"\b(brief|short|concise).*(message|communication)\b", re.IGNORECASE),
            "works late": re.compile(r"\b(work|working).*(late|night)\b", re.IGNORECASE),
            "pet": re.compile(r"\b(cat|dog|pet)\b(?:\s+(\w+))?", re.IGNORECASE),
            "prefer text": re.compile(r"\bprefer.*(text|async|writing)\b", re.IGNORECASE),
            "direct communication": re.compile(r"\bdirect\s+communication\b", re.IGNORECASE),
            "early bird": re.compile(r"\b(morning person|early bird|wake up early)\b", re.IGNORECASE),
            "introvert": re.compile(r"\b(introvert|introverted|prefer alone time)\b", re.IGNORECASE),
            "extrovert": re.compile(r"\b(extrovert|extroverted|love socializing)\b", re.IGNORECASE),
            "remote work": re.compile(r"\b(remote work|work from home|wfh)\b", re.IGNORECASE),
            "coffee lover": re.compile(r"\b(love coffee|coffee addict|need coffee)\b", re.IGNORECASE),
            "tea lover": re.compile(r"\b(love tea|tea person|prefer tea)\b", re.IGNORECASE),
            "exercise": re.compile(r"\b(gym|workout|exercise|fitness)\b", re.IGNORECASE),
            "reading": re.compile(r"\b(love reading|enjoy books|bookworm)\b", re.IGNORECASE),
        }
        
        self.emotional_keywords = {
            "stress": re.compile(r"\b(stressed|anxious|overwhelmed|frustrated)\b", re.IGNORECASE),
            "appreciation": re.compile(r"\b(appreciate|grateful|thankful)\b", re.IGNORECASE),
            "overthinking": re.compile(r"\boverthink\b", re.IGNORECASE),
            "excited": re.compile(r"\b(excited|thrilled|looking forward)\b", re.IGNORECASE),
            "tired": re.compile(r"\b(tired|exhausted|burned out)\b", re.IGNORECASE),
            "happy": re.compile(r"\b(happy|joyful|delighted)\b", re.IGNORECASE),
            "confused": re.compile(r"\b(confused|unsure|uncertain)\b", re.IGNORECASE),
        }
    
    def extract(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        preferences = []
        emotional_patterns = []
        facts = []
        raw_extractions = []
        
        seen_preferences = set()
        seen_emotions = set()
        seen_facts = set()
        
        for msg in messages:
            if msg.get("role") != "user":
                continue
                
            idx = msg["index"]
            content = msg["content"]
            
            for pref_name, pattern in self.patterns.items():
                match = pattern.search(content)
                if match:
                    pref_key = f"{pref_name}:{match.group(0).lower()}"
                    if pref_key not in seen_preferences:
                        seen_preferences.add(pref_key)
                        
                        if pref_name == "allergic":
                            allergen = match.group(1)
                            preferences.append({
                                "category": "health",
                                "value": f"allergic to {allergen}",
                                "confidence": 0.95,
                                "source_messages": [idx]
                            })
                        elif pref_name == "pet":
                            pet_type = match.group(1)
                            pet_name = match.group(2) if match.lastindex >= 2 else None
                            value = f"has {pet_type}"
                            if pet_name:
                                value = f"has {pet_type} named {pet_name}"
                            preferences.append({
                                "category": "lifestyle",
                                "value": value,
                                "confidence": 0.90,
                                "source_messages": [idx]
                            })
                        else:
                            category = self._categorize_preference(pref_name)
                            preferences.append({
                                "category": category,
                                "value": pref_name.replace("_", " "),
                                "confidence": 0.85,
                                "source_messages": [idx]
                            })
            
            for emotion, pattern in self.emotional_keywords.items():
                if pattern.search(content):
                    if emotion not in seen_emotions:
                        seen_emotions.add(emotion)
                        emotional_patterns.append({
                            "pattern": emotion,
                            "confidence": 0.80,
                            "source_messages": [idx]
                        })
            
            doc = self.nlp(content)
            for ent in doc.ents:
                fact_key = f"{ent.label_}:{ent.text.lower()}"
                if fact_key not in seen_facts:
                    seen_facts.add(fact_key)
                    
                    fact_type = self._map_entity_to_fact_type(ent.label_)
                    facts.append({
                        "fact_type": fact_type,
                        "value": ent.text,
                        "confidence": 0.88,
                        "source_messages": [idx]
                    })
                    
                    raw_extractions.append({
                        "text": ent.text,
                        "message_index": idx,
                        "entity_type": ent.label_
                    })
        
        memory = {
            "user_id": "default_user",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "preferences": preferences,
            "emotional_patterns": emotional_patterns,
            "facts": facts,
            "raw_extractions": raw_extractions
        }
        
        return memory
    
    def _categorize_preference(self, pref_name: str) -> str:
        category_map = {
            "vegetarian": "food",
            "lo-fi": "music",
            "green tea": "food",
            "async": "work_style",
            "hates meetings": "work_style",
            "linux": "technology",
            "short messages": "communication",
            "works late": "work_style",
            "prefer text": "communication",
            "direct communication": "communication",
            "early bird": "work_style",
            "introvert": "personality",
            "extrovert": "personality",
            "remote work": "work_style",
            "coffee lover": "food",
            "tea lover": "food",
            "exercise": "lifestyle",
            "reading": "hobby",
        }
        return category_map.get(pref_name, "general")
    
    def _map_entity_to_fact_type(self, entity_label: str) -> str:
        mapping = {
            "GPE": "location",
            "LOC": "location",
            "DATE": "date",
            "TIME": "time",
            "PERSON": "person",
            "ORG": "organization",
            "PRODUCT": "product",
            "EVENT": "event",
            "LANGUAGE": "language",
        }
        return mapping.get(entity_label, "general")