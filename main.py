from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging

from backend.app.extraction import Extractor
from backend.app.validators import validate_memory, ValidationError
from backend.app.personality import PersonalityEngine
from backend.app.llm_client import LLMClient, NoLLMAvailable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Memory Extraction & Personality API",
    description="Extract memories from conversations and rewrite with personality",
    version="1.0.0"
)

extractor = Extractor()
personality_engine = PersonalityEngine()
llm_client = LLMClient()


class Message(BaseModel):
    index: int
    role: str
    content: str


class ExtractRequest(BaseModel):
    messages: List[Message]
    use_llm: bool = Field(default=False, description="Use LLM for extraction if available")


class RewriteRequest(BaseModel):
    text: str
    personality: str = Field(..., description="One of: calm_mentor, witty_friend, therapist")
    use_llm: bool = Field(default=False, description="Use LLM for rewriting if available")


@app.get("/")
def root():
    return {
        "message": "Memory Extraction & Personality API",
        "endpoints": {
            "POST /extract": "Extract memories from messages",
            "POST /rewrite": "Rewrite text with personality",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "llm_available": llm_client.is_available(),
        "components": {
            "extractor": "operational",
            "personality_engine": "operational",
            "validator": "operational"
        }
    }


@app.post("/extract")
def extract_memories(request: ExtractRequest):
    try:
        messages_list = [msg.model_dump() for msg in request.messages]
        
        if request.use_llm and llm_client.is_available():
            logger.info("Using LLM for extraction")
            try:
                memory = llm_client.extract_memories(messages_list)
            except NoLLMAvailable as e:
                logger.warning(f"LLM extraction failed: {e}. Falling back to deterministic.")
                memory = extractor.extract(messages_list)
        else:
            logger.info("Using deterministic extraction")
            memory = extractor.extract(messages_list)
        
        try:
            validate_memory(memory)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=f"Memory validation failed: {str(e)}")
        
        return {
            "success": True,
            "memory": memory,
            "method": "llm" if (request.use_llm and llm_client.is_available()) else "deterministic"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rewrite")
def rewrite_text(request: RewriteRequest):
    valid_personalities = ["calm_mentor", "witty_friend", "therapist"]
    if request.personality not in valid_personalities:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid personality. Must be one of: {', '.join(valid_personalities)}"
        )
    
    try:
        if request.use_llm and llm_client.is_available():
            logger.info(f"Using LLM for rewriting with personality: {request.personality}")
            try:
                rewritten = llm_client.rewrite_with_personality(request.text, request.personality)
            except NoLLMAvailable as e:
                logger.warning(f"LLM rewrite failed: {e}. Falling back to deterministic.")
                rewritten = personality_engine.rewrite(request.text, request.personality)
        else:
            logger.info(f"Using deterministic rewriting with personality: {request.personality}")
            rewritten = personality_engine.rewrite(request.text, request.personality)
        
        return {
            "success": True,
            "original": request.text,
            "rewritten": rewritten,
            "personality": request.personality,
            "method": "llm" if (request.use_llm and llm_client.is_available()) else "deterministic"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rewrite error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)