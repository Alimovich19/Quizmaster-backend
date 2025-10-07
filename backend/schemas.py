from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ================== USER SCHEMAS ==================
class UserBase(BaseModel):
    email: EmailStr
    nickname: str
    name: str


class UserCreate(UserBase):
    password: str
    role: str = "player"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None
    profile_picture: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: str
    profile_picture: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True   # ✅ Pydantic v2 uchun


# ================== AUTH SCHEMAS ==================
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ================== QUIZ SCHEMAS ==================
class QuestionSchema(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: int = Field(..., alias="correctAnswer")  # ✅ frontend camelCase

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "12345",
                "question": "What is 2 + 2?",
                "options": ["1", "2", "3", "4"],
                "correctAnswer": 3
            }
        }


class QuizCreate(BaseModel):
    title: str
    questions: List[QuestionSchema]


class QuizResponse(BaseModel):
    id: int
    title: str
    game_code: str
    questions: List[QuestionSchema]
    creator_id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ================== QUIZ HISTORY SCHEMAS ==================
class QuizHistoryCreate(BaseModel):
    quiz_id: int
    quiz_title: str
    score: int
    total_questions: int
    rank: int
    participants_count: int


class QuizHistoryResponse(BaseModel):
    id: int
    quiz_title: str
    score: int
    total_questions: int
    rank: int
    participants_count: int
    played_at: datetime

    class Config:
        from_attributes = True


# ================== GAME SESSION SCHEMAS ==================
class JoinGameRequest(BaseModel):
    game_code: str
    player_name: str


class GameSessionResponse(BaseModel):
    id: int
    game_code: str
    quiz_id: int
    host_id: Optional[int]
    players: List[str]
    status: str
    is_active: bool                # ✅ yangi qo‘shilgan
    created_at: datetime
    quiz: Optional[QuizResponse] = None  # ✅ related quiz response uchun

    class Config:
        from_attributes = True