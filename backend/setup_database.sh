#!/bin/bash

# ============================================
# Quiz Game - Database Setup Script
# ============================================

echo ""
echo "============================================"
echo "  Quiz Game - Database Setup"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if MySQL is running
echo -e "${BLUE}[1/4] MySQL'ni tekshirmoqda...${NC}"
if lsof -i :8889 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ MAMP MySQL ishlayapti (port 8889)${NC}"
    MYSQL_PORT=8889
    MYSQL_CMD="mysql -u root -proot -P 8889 -h 127.0.0.1"
elif lsof -i :3306 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ MySQL ishlayapti (port 3306)${NC}"
    MYSQL_PORT=3306
    MYSQL_CMD="mysql -u root -proot"
else
    echo -e "${RED}❌ MySQL ishlamayapti!${NC}"
    echo -e "${YELLOW}Iltimos MAMP'ni ishga tushiring${NC}"
    exit 1
fi

echo ""

# Create database
echo -e "${BLUE}[2/4] Database yaratilmoqda...${NC}"
$MYSQL_CMD -e "CREATE DATABASE IF NOT EXISTS quiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ quiz_db database yaratildi${NC}"
else
    echo -e "${RED}❌ Database yaratishda xato${NC}"
    echo -e "${YELLOW}phpMyAdmin orqali qo'lda yarating: http://localhost:8888/phpMyAdmin/${NC}"
fi

echo ""

# Check if Python virtual environment exists
echo -e "${BLUE}[3/4] Python environment'ni tekshirmoqda...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment topilmadi, yaratilmoqda...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

echo ""

# Install dependencies if needed
if ! python -c "import sqlalchemy" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies o'rnatilmoqda...${NC}"
    pip install -r requirements.txt > /dev/null 2>&1
fi

# Create tables using Python
echo -e "${BLUE}[4/4] Tables yaratilmoqda...${NC}"
python create_tables.py

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}  ✅ Database tayyor!${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    echo "Keyingi qadamlar:"
    echo ""
    echo "1. Backend serverni ishga tushiring:"
    echo "   ${YELLOW}uvicorn main:app --reload${NC}"
    echo ""
    echo "2. Yangi terminal ochib, frontend'ni ishga tushiring:"
    echo "   ${YELLOW}npm run dev${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}============================================${NC}"
    echo -e "${RED}  ❌ Xato!${NC}"
    echo -e "${RED}============================================${NC}"
    echo ""
    echo "Muammo hal qilish:"
    echo "1. .env faylni tekshiring"
    echo "2. MySQL ulanish ma'lumotlarini to'g'rilang"
    echo "3. MAMP_SETUP.md faylni o'qing"
    echo ""
fi