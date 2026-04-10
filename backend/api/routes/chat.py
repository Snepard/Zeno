from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ai_engine.chatbot.chat_handler import handle_chat
from api.deps import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    job_id: str
    question: str
    current_slide: Optional[int] = None
    mode: str = "doubt"  # Modes explicitly tracked natively (doubt, summarize, quiz, explain_simple)

class ChatResponse(BaseModel):
    answer: str
    source_chunks: list

@router.post("/", response_model=ChatResponse)
async def process_chat(req: ChatRequest, current_user: dict = Depends(get_current_user)):
    """
    RAG-driven native Question-Processing pipeline mapping perfectly onto pre-generated
    AI Jobs. Bypasses pure GPT hallucination securely explicitly relying solely upon chunk data constraints.
    """
    try:
        # User auth routing
        user_id = str(current_user.get("sub", current_user.get("user_id", "unknown")))
        
        result = handle_chat(
            job_id=req.job_id, 
            user_id=user_id, 
            question=req.question, 
            current_slide=req.current_slide, 
            mode=req.mode
        )
        return result
    except Exception as e:
        logger.error(f"Native Chat Execution Pipeline crashed heavily: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
