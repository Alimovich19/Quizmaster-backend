from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)  # max 255
    nickname = Column(String(100), unique=True, index=True, nullable=False)  # max 100
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="player")  # admin or player
    profile_picture = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    created_quizzes = relationship("Quiz", back_populates="creator")
    quiz_history = relationship("QuizHistory", back_populates="user")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    game_code = Column(String(20), unique=True, index=True, nullable=False)  # game_code uchun kifoya
    questions = Column(JSON, nullable=False)  # Store as JSON
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    creator = relationship("User", back_populates="created_quizzes")
    participants = relationship("QuizHistory", back_populates="quiz")


class QuizHistory(Base):
    __tablename__ = "quiz_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    quiz_title = Column(String(255))  # max 255
    score = Column(Integer)
    total_questions = Column(Integer)
    rank = Column(Integer)
    participants_count = Column(Integer)
    played_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="quiz_history")
    quiz = relationship("Quiz", back_populates="participants")


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    game_code = Column(String(20), unique=True, index=True)  # max 20 chars
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    host_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=False)
    players = Column(JSON, default=[])  # List of player names
    status = Column(String(20), default="waiting")  # waiting, playing, finished
    created_at = Column(DateTime, default=datetime.utcnow)