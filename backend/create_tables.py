#!/usr/bin/env python3
"""
Database Tables Yaratish Script

Bu script barcha database tables'ni avtomatik yaratadi.

Usage:
    python create_tables.py
"""

import sys
from database import engine, Base
from models import User, Quiz, QuizHistory, GameSession

def create_tables():
    """Create all database tables"""
    print("=" * 60)
    print("  Quiz Game - Database Tables Yaratish")
    print("=" * 60)
    print()
    
    try:
        print("📊 Database'ga ulanmoqda...")
        # Test connection
        with engine.connect() as conn:
            print("✅ Database ulandi!")
            print(f"   Database: {engine.url.database}")
            print(f"   Host: {engine.url.host}")
            print(f"   Port: {engine.url.port}")
            print()
        
        print("🏗️  Tables yaratilmoqda...")
        print()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Show created tables
        print("✅ Quyidagi tables yaratildi:")
        print()
        print("   1. users")
        print("      - id (PRIMARY KEY)")
        print("      - email (UNIQUE)")
        print("      - nickname (UNIQUE)")
        print("      - name")
        print("      - password_hash")
        print("      - role (admin/player)")
        print("      - profile_picture")
        print("      - created_at")
        print()
        
        print("   2. quizzes")
        print("      - id (PRIMARY KEY)")
        print("      - title")
        print("      - description")
        print("      - creator_id (FOREIGN KEY → users)")
        print("      - game_code (UNIQUE)")
        print("      - questions (JSON)")
        print("      - created_at")
        print("      - is_active")
        print()
        
        print("   3. quiz_history")
        print("      - id (PRIMARY KEY)")
        print("      - user_id (FOREIGN KEY → users)")
        print("      - quiz_id (FOREIGN KEY → quizzes)")
        print("      - score")
        print("      - total_questions")
        print("      - rank")
        print("      - participants")
        print("      - completed_at")
        print()
        
        print("   4. game_sessions")
        print("      - id (PRIMARY KEY)")
        print("      - quiz_id (FOREIGN KEY → quizzes)")
        print("      - game_code (UNIQUE)")
        print("      - host_id (FOREIGN KEY → users)")
        print("      - status (waiting/playing/finished)")
        print("      - players (JSON)")
        print("      - created_at")
        print()
        
        print("=" * 60)
        print("🎉 SUCCESS! Barcha tables muvaffaqiyatli yaratildi!")
        print("=" * 60)
        print()
        print("Keyingi qadam:")
        print("  1. Backend serverni ishga tushiring:")
        print("     cd backend")
        print("     uvicorn main:app --reload")
        print()
        print("  2. Frontend serverni ishga tushiring:")
        print("     npm run dev")
        print()
        print("  3. Brauzerda oching: http://localhost:5173")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("❌ XATO!")
        print("=" * 60)
        print(f"Xato: {str(e)}")
        print()
        print("Tekshirish:")
        print("  1. MAMP ishlamoqdami?")
        print("  2. MySQL server yashilmi? (Port 8889 yoki 3306)")
        print("  3. 'quiz_db' database yaratilganmi?")
        print("  4. .env fayl to'g'ri sozlanganmi?")
        print()
        print("Yordam uchun MAMP_SETUP.md faylini o'qing")
        print("=" * 60)
        return False

def drop_tables():
    """Drop all tables (DANGER!)"""
    print()
    print("⚠️  OGOHLANTIRISH!")
    print("=" * 60)
    print("Bu barcha tables va ma'lumotlarni o'chiradi!")
    print("=" * 60)
    confirm = input("Davom etishni xohlaysizmi? (yes/no): ")
    
    if confirm.lower() == 'yes':
        print()
        print("🗑️  Tables o'chirilmoqda...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Barcha tables o'chirildi!")
        print()
    else:
        print("❌ Bekor qilindi")
        print()

if __name__ == "__main__":
    print()
    
    # Check for drop command
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_tables()
    
    # Create tables
    success = create_tables()
    
    # Exit code
    sys.exit(0 if success else 1)