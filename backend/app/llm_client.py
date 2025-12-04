import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class NoLLMAvailable(Exception):
    pass


class LLMClient:
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key and self.api_key != "your-openai-api-key-here":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise NoLLMAvailable("openai package not installed")
            except Exception as e:
                raise NoLLMAvailable(f"Failed to initialize OpenAI client: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def extract_memories(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.is_available():
            raise NoLLMAvailable("LLM not available for extraction")
        
        messages_text = "\n".join([
            f"[{msg['index']}] {msg['role']}: {msg['content']}"
            for msg in messages if msg.get('role') == 'user'
        ])
        
        prompt = f"""Analyze the following user messages and extract structured information.
        
Messages:
{messages_text}

Extract:
1. Preferences (food, work style, communication, technology, lifestyle)
2. Emotional patterns (stress, anxiety, appreciation, etc.)
3. Facts (locations, dates, people, organizations)

Return a JSON object with:
- preferences: array of {{category, value, confidence, source_messages}}
- emotional_patterns: array of {{pattern, confidence, source_messages}}
- facts: array of {{fact_type, value, confidence, source_messages}}

Be specific and include message indices in source_messages."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a memory extraction assistant. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            result["user_id"] = "default_user"
            from datetime import datetime
            result["generated_at"] = datetime.utcnow().isoformat() + "Z"
            result["raw_extractions"] = []
            
            return result
            
        except Exception as e:
            raise NoLLMAvailable(f"LLM extraction failed: {e}")
    
    def rewrite_with_personality(self, text: str, personality: str) -> str:
        if not self.is_available():
            raise NoLLMAvailable("LLM not available for rewriting")
        
        personality_prompts = {
            "calm_mentor": "Rewrite this in a calm, thoughtful, mentor-like tone. Be gentle and encouraging.",
            "witty_friend": "Rewrite this in a casual, witty, friendly tone. Add some humor and emojis.",
            "therapist": "Rewrite this in a validating, empathetic therapist tone. Add reflective questions."
        }
        
        if personality not in personality_prompts:
            raise ValueError(f"Unknown personality: {personality}")
        
        prompt = personality_prompts[personality]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Rewrite this: {text}"}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise NoLLMAvailable(f"LLM rewrite failed: {e}")
    
    def close(self):
        if self.client:
            self.client = None