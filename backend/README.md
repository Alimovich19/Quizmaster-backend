# Quiz Game Backend - FastAPI + MySQL

Bu loyihaning backend qismi. MySQL (MAMP) + FastAPI yordamida yaratilgan.

## 📋 O'rnatish - MAMP bilan

### 1. MAMP o'rnatish va sozlash

**MAMP yuklab olish:**
- macOS: https://www.mamp.info/en/downloads/
- Windows: https://www.mamp.info/en/downloads/

**MAMP sozlash:**
1. MAMP'ni ishga tushiring
2. MySQL portini tekshiring (odatda 8889, ba'zan 3306)
3. phpMyAdmin'ga kiring: http://localhost:8888/phpMyAdmin/

### 2. MySQL Database yaratish

**phpMyAdmin orqali:**

1. phpMyAdmin'ga kiring: http://localhost:8888/phpMyAdmin/
2. Username: `root`, Password: `root` (MAMP default)
3. Yangi database yarating:
   - "New" tugmasini bosing
   - Database nomi: `quiz_db`
   - Collation: `utf8mb4_general_ci`
   - "Create" bosing

**Yoki MySQL command line orqali:**

```bash
# MAMP MySQL ga ulanish
/Applications/MAMP/Library/bin/mysql -u root -p
# Password: root

# Database yaratish
CREATE DATABASE quiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
SHOW DATABASES;
EXIT;
```

### 3. Backend proyektni sozlash

```bash
# Backend papkasiga kiring
cd backend

# Virtual environment yaratish
python3 -m venv venv

# Virtual environment ni aktivlashtirish
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Dependencies o'rnatish
pip install -r requirements.txt
```

### 4. Environment o'zgaruvchilarni sozlash

`.env` faylini yarating:

```bash
cp .env.example .env
```

**MAMP uchun `.env` fayl** (port 8889):
```env
DATABASE_URL=mysql+pymysql://root:root@localhost:8889/quiz_db
SECRET_KEY=your-random-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
```

**Standard MySQL uchun** (port 3306):
```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/quiz_db
SECRET_KEY=your-random-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
```

### 5. Database tablelarni yaratish

Backend server birinchi marta ishga tushganda, tablelar avtomatik yaratiladi.

```bash
# Virtual env aktivligi holatda
python -c "from database import engine, Base; from models import *; Base.metadata.create_all(bind=engine); print('✅ Tables created!')"
```

### 6. Serverni ishga tushirish

```bash
# Backend papkasida
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend ishga tushdi:
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🔍 MAMP MySQL Portini Topish

MAMP MySQL porti 8889 yoki 3306 bo'lishi mumkin:

**1-usul - MAMP Preferences:**
- MAMP'ni oching
- Preferences → Ports
- MySQL Port: ko'rsatilgan raqam

**2-usul - phpMyAdmin:**
- http://localhost:8888/phpMyAdmin/
- Yuqori qismda server ma'lumotlari ko'rinadi

**3-usul - Command line:**
```bash
lsof -i :8889
lsof -i :3306
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Ro'yxatdan o'tish
- `POST /api/auth/login` - Kirish
- `GET /api/auth/me` - Joriy foydalanuvchi
- `PUT /api/auth/profile` - Profilni yangilash

### Quiz
- `POST /api/quiz/create` - Yangi quiz yaratish
- `GET /api/quiz/{game_code}` - Quiz ma'lumotlarini olish
- `GET /api/quiz/user/created` - Foydalanuvchi yaratgan quizlar

### Game Session
- `POST /api/game/join` - O'yinga qo'shilish
- `GET /api/game/{game_code}/session` - O'yin sessiyasi

### History
- `POST /api/history/add` - Quiz tarixini saqlash
- `GET /api/history/me` - O'z tarixingiz

## 🔧 Troubleshooting

### MySQL ulanish xatosi

**1. MAMP ishga tushganini tekshiring:**
- MAMP'ni oching
- MySQL'ning yashil chiroq yonganini ko'ring

**2. Portni tekshiring:**
```bash
# .env faylda to'g'ri port yozilganini tekshiring
# MAMP default: 8889
# Standard MySQL: 3306
```

**3. MySQL ulanishni test qiling:**
```bash
# MAMP MySQL
/Applications/MAMP/Library/bin/mysql -u root -proot -h localhost -P 8889

# Standard MySQL
mysql -u root -p -h localhost -P 3306
```

**4. Database mavjudligini tekshiring:**
```sql
SHOW DATABASES;
USE quiz_db;
SHOW TABLES;
```

### Port band

```bash
# 8000 portni band qilgan processni toping
lsof -i :8000
# Process ni to'xtating
kill -9 <PID>
```

### PyMySQL o'rnatilmagan

```bash
pip install PyMySQL
# yoki
pip install -r requirements.txt
```

### Table yaratilmagan

```bash
# Qo'lda yaratish
python -c "from database import engine, Base; from models import *; Base.metadata.create_all(bind=engine)"
```

## 📊 Database Ma'lumotlarini Ko'rish

### phpMyAdmin orqali:
1. http://localhost:8888/phpMyAdmin/
2. `quiz_db` ni tanlang
3. Tablelarni ko'ring: `users`, `quizzes`, `quiz_history`, `game_sessions`

### MySQL Command Line orqali:
```bash
# MAMP MySQL
/Applications/MAMP/Library/bin/mysql -u root -proot quiz_db

# Tablelarni ko'rish
SHOW TABLES;

# Users ko'rish
SELECT * FROM users;

# Quizzes ko'rish
SELECT * FROM quizzes;
```

## 🚀 To'liq Ishga Tushirish Tartibi

### 1. MAMP ishga tushirish
- MAMP'ni oching
- "Start" tugmasini bosing
- MySQL yashil bo'lguncha kuting

### 2. Database yaratish (birinchi marta)
- phpMyAdmin: http://localhost:8888/phpMyAdmin/
- Database: `quiz_db` yaratish

### 3. Backend ishga tushirish
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test qilish
```bash
# Health check
curl http://localhost:8000/health

# API Docs
# Browser: http://localhost:8000/docs
```

## ✅ Muvaffaqiyatli O'rnatish

Agar hammasi to'g'ri bo'lsa:

1. ✅ MAMP MySQL ishlamoqda
2. ✅ Database `quiz_db` yaratilgan
3. ✅ Backend: http://localhost:8000/docs
4. ✅ Health: http://localhost:8000/health
5. ✅ Tables avtomatik yaratilgan

**Keyingi qadam:** Frontend'ni ulash! 🎉
