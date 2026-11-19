from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Auth schemas
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# AI schemas
class ChatMessage(BaseModel):
    message: str
    conversation_history: list[dict] = []


class ChatResponse(BaseModel):
    reply: str
    conversation_history: list[dict]


class TextAnalysisRequest(BaseModel):
    text: str
    mode: str = "summarise"  # summarise | sentiment | keypoints | all


class TextAnalysisResponse(BaseModel):
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    key_points: Optional[list[str]] = None
    word_count: int


class ImageAnalysisRequest(BaseModel):
    image_base64: str
    question: str = "Describe this image in detail"


class ImageAnalysisResponse(BaseModel):
    answer: str
