from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.deps import get_current_user
from ai_engine.chatbot.chat_handler import handle_chat
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    job_id: str
    question: str
    current_slide: Optional[int] = 0
    mode: str = "doubt"


@router.post("/")
async def chat(req: ChatRequest, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        result = handle_chat(
            job_id=req.job_id,
            user_id=user_id,
            question=req.question,
            current_slide=req.current_slide,
            mode=req.mode,
        )
        return result
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
