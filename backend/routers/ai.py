from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from auth import get_current_user
from schemas import (
    ChatMessage, ChatResponse,
    TextAnalysisRequest, TextAnalysisResponse,
    ImageAnalysisRequest, ImageAnalysisResponse
)
from services.claude_service import chat, analyse_text, analyse_image
import google.generativeai as genai

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def ai_chat(data: ChatMessage, current_user: User = Depends(get_current_user)):
    """Send a message to the AI assistant."""
    try:
        reply, history = chat(data.message, data.conversation_history)
        return {"reply": reply, "conversation_history": history}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")


@router.post("/analyse-text", response_model=TextAnalysisResponse)
def ai_analyse_text(data: TextAnalysisRequest, current_user: User = Depends(get_current_user)):
    """Analyse text — summarise, sentiment, key points, or all."""
    if len(data.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text too short to analyse")
    if len(data.text) > 10000:
        raise HTTPException(status_code=400, detail="Text too long (max 10,000 characters)")

    valid_modes = ["summarise", "sentiment", "keypoints", "all"]
    if data.mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Mode must be one of: {valid_modes}")

    try:
        result = analyse_text(data.text, data.mode)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")


@router.post("/analyse-image", response_model=ImageAnalysisResponse)
def ai_analyse_image(data: ImageAnalysisRequest, current_user: User = Depends(get_current_user)):
    """Answer a question about an uploaded image."""
    if not data.image_base64:
        raise HTTPException(status_code=400, detail="No image provided")

    try:
        answer = analyse_image(data.image_base64, data.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")
