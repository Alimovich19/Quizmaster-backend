from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import Quiz, GameSession
from schemas import GameSessionResponse, JoinGameRequest

router = APIRouter(prefix="/api/game", tags=["Game Sessions"])


# 🎮 1️⃣ O‘yinni boshlash yoki mavjudini faollashtirish
@router.post("/start/{game_code}", response_model=GameSessionResponse)
def start_game_session(game_code: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.game_code == game_code).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Mavjud sessiyani tekshirish
    session = db.query(GameSession).filter(GameSession.game_code == game_code).first()

    if not session:
        # 🔹 Yangi session yaratish
        session = GameSession(
            game_code=game_code,
            quiz_id=quiz.id,
            host_id=quiz.creator_id,  # ✅ kim yaratganini yozamiz
            created_at=datetime.utcnow(),
            players=[],
            status="waiting",
            is_active=True,
        )
        db.add(session)
    else:
        # 🔹 Mavjud sessiyani qayta faollashtirish
        session.is_active = True
        session.status = "waiting"
        session.created_at = datetime.utcnow()

    # 🔹 Faqat shu quiz aktiv bo‘lsin
    db.query(Quiz).update({Quiz.is_active: False})
    quiz.is_active = True

    db.commit()
    db.refresh(session)
    return session


# 🙋 2️⃣ O‘yinchi faqat faol sessiyaga qo‘shilishi mumkin
@router.post("/join", response_model=GameSessionResponse)
def join_game(request: JoinGameRequest, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(
        GameSession.game_code == request.game_code,
        GameSession.is_active == True
    ).first()

    if not session:
        raise HTTPException(
            status_code=400,
            detail="This game is not active. Wait for the host to start it."
        )

    # 🔹 O‘yinchi ro‘yxatga qo‘shiladi
    players = session.players or []
    if request.player_name not in players:
        players.append(request.player_name)
        session.players = players

    session.status = "waiting"
    db.commit()
    db.refresh(session)

    return session


# 🧊 3️⃣ Sessionni olish (Frontend uchun)
@router.get("/{game_code}/session", response_model=GameSessionResponse)
def get_game_session(game_code: str, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.game_code == game_code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")

    return session


# 🛑 4️⃣ O‘yinni tugatish
@router.patch("/end/{game_code}")
def end_game_session(game_code: str, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.game_code == game_code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")

    quiz = db.query(Quiz).filter(Quiz.game_code == game_code).first()

    session.is_active = False
    session.status = "finished"
    if quiz:
        quiz.is_active = False

    db.commit()
    return {
        "message": "Game session ended successfully",
        "game_code": game_code
    }