from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import random
import string

from database import engine, get_db, Base
from models import User, Quiz, QuizHistory, GameSession
from schemas import (
    UserCreate, UserResponse, UserUpdate, Token, LoginRequest,
    QuizCreate, QuizResponse, QuizHistoryCreate, QuizHistoryResponse,
    JoinGameRequest, GameSessionResponse
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create database tables
Base.metadata.create_all(bind=engine)
from routes import game_routes


app = FastAPI(title="Quiz Game API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_routes.router)
# Generate random game code
def generate_game_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.nickname == user_data.nickname).first():
        raise HTTPException(status_code=400, detail="Nickname already taken")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        nickname=user_data.nickname,
        name=user_data.name,
        hashed_password=hashed_password,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user_id=new_user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }


@app.post("/api/auth/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user_id=user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/api/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.put("/api/auth/profile", response_model=UserResponse)
def update_profile(
        updates: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if updates.name:
        current_user.name = updates.name
    if updates.nickname:
        existing = db.query(User).filter(
            User.nickname == updates.nickname,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Nickname already taken")
        current_user.nickname = updates.nickname
    if updates.profile_picture:
        current_user.profile_picture = updates.profile_picture

    db.commit()
    db.refresh(current_user)
    return current_user


# ==================== QUIZ ENDPOINTS ====================

@app.post("/api/quiz/create", response_model=QuizResponse)
def create_quiz(
        quiz_data: QuizCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    game_code = generate_game_code()
    while db.query(Quiz).filter(Quiz.game_code == game_code).first():
        game_code = generate_game_code()

    # ✅ alias bilan saqlash
    questions_dict = [q.dict(by_alias=True) for q in quiz_data.questions]

    new_quiz = Quiz(
        title=quiz_data.title,
        game_code=game_code,
        questions=questions_dict,
        creator_id=current_user.id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return new_quiz


@app.get("/api/quiz/{game_code}", response_model=QuizResponse)
def get_quiz(game_code: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.game_code == game_code).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@app.get("/api/quiz/user/created", response_model=List[QuizResponse])
def get_user_quizzes(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    quizzes = db.query(Quiz).filter(Quiz.creator_id == current_user.id).all()
    return quizzes


# ==================== GAME SESSION ENDPOINTS ====================

@app.post("/api/game/start/{game_code}")
def start_game(
        game_code: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(Quiz.game_code == game_code).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the host can start the game")

    quiz.is_active = True
    db.commit()
    db.refresh(quiz)

    return {"message": "Game started", "game_code": quiz.game_code}


@app.post("/api/game/join", response_model=GameSessionResponse)
def join_game(
        join_data: JoinGameRequest,
        db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(Quiz.game_code == join_data.game_code).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Game not found")

    if not quiz.is_active:
        raise HTTPException(status_code=403, detail="Game is not active")

    session = db.query(GameSession).filter(GameSession.game_code == join_data.game_code).first()
    if not session:
        session = GameSession(
            game_code=join_data.game_code,
            quiz_id=quiz.id,
            host_id=quiz.creator_id,
            players=[join_data.player_name]
        )
        db.add(session)
    else:
        players = session.players or []
        if join_data.player_name not in players:
            players.append(join_data.player_name)
            session.players = players

    db.commit()
    db.refresh(session)

    return {
        "game_code": session.game_code,
        "players": session.players,
        "status": session.status,
        "host_id": session.host_id,
        "quiz": quiz
    }


@app.get("/api/game/{game_code}/session", response_model=GameSessionResponse)
def get_game_session(game_code: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.game_code == game_code).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Game not found")

    if not quiz.is_active:
        raise HTTPException(status_code=403, detail="Game is not active")

    session = db.query(GameSession).filter(GameSession.game_code == game_code).first()
    if not session:
        session = GameSession(
            game_code=game_code,
            quiz_id=quiz.id,
            host_id=quiz.creator_id,
            players=[]
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    return session


# ==================== QUIZ HISTORY ENDPOINTS ====================

@app.post("/api/history/add")
def add_quiz_history(
        history_data: QuizHistoryCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    new_history = QuizHistory(
        user_id=current_user.id,
        quiz_id=history_data.quiz_id,
        quiz_title=history_data.quiz_title,
        score=history_data.score,
        total_questions=history_data.total_questions,
        rank=history_data.rank,
        participants_count=history_data.participants_count
    )
    db.add(new_history)
    db.commit()
    return {"message": "History saved successfully"}


@app.get("/api/history/me", response_model=List[QuizHistoryResponse])
def get_my_history(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    history = db.query(QuizHistory).filter(
        QuizHistory.user_id == current_user.id
    ).order_by(QuizHistory.played_at.desc()).all()
    return history


# ==================== HEALTH CHECK ====================

@app.get("/")
def root():
    return {"message": "Quiz Game API is running", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}