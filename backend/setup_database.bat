@echo off
REM ============================================
REM Quiz Game - Database Setup Script (Windows)
REM ============================================

echo.
echo ============================================
echo   Quiz Game - Database Setup
echo ============================================
echo.

REM [1/4] Check MySQL
echo [1/4] MySQL tekshirilmoqda...
netstat -an | find ":3306" >nul
if errorlevel 1 (
    netstat -an | find ":8889" >nul
    if errorlevel 1 (
        echo [ERROR] MySQL ishlamayapti!
        echo Iltimos MAMP yoki MySQL serverni ishga tushiring
        pause
        exit /b 1
    ) else (
        echo [OK] MAMP MySQL ishlayapti (port 8889)
        set MYSQL_PORT=8889
    )
) else (
    echo [OK] MySQL ishlayapti (port 3306)
    set MYSQL_PORT=3306
)

echo.

REM [2/4] Create database
echo [2/4] Database yaratilmoqda...
REM User qo'lda yaratishi kerak chunki Windows'da MySQL CLI muammoli
echo [INFO] phpMyAdmin'da qo'lda database yarating:
echo        URL: http://localhost:8888/phpMyAdmin/
echo        Database name: quiz_db
echo        Collation: utf8mb4_unicode_ci
echo.
echo Database yaratdingizmi? (y/n)
set /p CREATED="> "
if /i not "%CREATED%"=="y" (
    echo.
    echo [WARNING] Database yaratilmadi. Iltimos phpMyAdmin'da yarating.
    pause
    exit /b 1
)

echo.

REM [3/4] Check Python virtual environment
echo [3/4] Python environment tekshirilmoqda...
if not exist "venv" (
    echo [INFO] Virtual environment yaratilmoqda...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

echo.

REM [4/4] Create tables
echo [4/4] Tables yaratilmoqda...
python create_tables.py

if errorlevel 1 (
    echo.
    echo ============================================
    echo   [ERROR] Xato!
    echo ============================================
    echo.
    echo Muammo hal qilish:
    echo 1. .env faylni tekshiring
    echo 2. MySQL ulanish ma'lumotlarini to'g'rilang
    echo 3. MAMP_SETUP.md faylni o'qing
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   [SUCCESS] Database tayyor!
echo ============================================
echo.
echo Keyingi qadamlar:
echo.
echo 1. Backend serverni ishga tushiring:
echo    uvicorn main:app --reload
echo.
echo 2. Yangi terminal ochib, frontend ishga tushiring:
echo    npm run dev
echo.
pause