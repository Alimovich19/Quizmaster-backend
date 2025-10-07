-- ============================================
-- Quiz Game - Database Initialization Script
-- ============================================
-- Bu SQL script barcha tables'ni yaratadi

-- Database yaratish (agar yo'q bo'lsa)
CREATE DATABASE IF NOT EXISTS quiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE quiz_db;

-- ============================================
-- 1. USERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    nickname VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'player') NOT NULL DEFAULT 'player',
    profile_picture TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_nickname (nickname),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 2. QUIZZES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS quizzes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    creator_id INT NOT NULL,
    game_code VARCHAR(20) NOT NULL UNIQUE,
    questions JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_game_code (game_code),
    INDEX idx_creator (creator_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 3. QUIZ_HISTORY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS quiz_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quiz_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,
    total_questions INT NOT NULL DEFAULT 0,
    rank INT NOT NULL DEFAULT 0,
    participants INT NOT NULL DEFAULT 0,
    completed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
    
    INDEX idx_user (user_id),
    INDEX idx_quiz (quiz_id),
    INDEX idx_completed (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 4. GAME_SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS game_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    game_code VARCHAR(20) NOT NULL UNIQUE,
    host_id INT NOT NULL,
    status ENUM('waiting', 'playing', 'finished') NOT NULL DEFAULT 'waiting',
    players JSON NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_game_code (game_code),
    INDEX idx_host (host_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- DEMO DATA (Optional)
-- ============================================
-- Uncomment quyidagi qatorlarni agar demo ma'lumotlar kerak bo'lsa

-- Demo user yaratish (password: admin123)
/*
INSERT INTO users (email, nickname, name, password_hash, role) VALUES 
('admin@quiz.com', 'admin', 'Admin User', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ND2xB7OlLF7u', 'admin');

INSERT INTO users (email, nickname, name, password_hash, role) VALUES 
('player@quiz.com', 'player1', 'Test Player', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ND2xB7OlLF7u', 'player');
*/

-- Demo quiz yaratish
/*
INSERT INTO quizzes (title, description, creator_id, game_code, questions) VALUES 
(
    'General Knowledge Quiz',
    'Test your general knowledge',
    1,
    'DEMO01',
    JSON_ARRAY(
        JSON_OBJECT(
            'id', '1',
            'question', 'What is the capital of France?',
            'options', JSON_ARRAY('London', 'Berlin', 'Paris', 'Madrid'),
            'correctAnswer', 2
        ),
        JSON_OBJECT(
            'id', '2',
            'question', 'Which planet is known as the Red Planet?',
            'options', JSON_ARRAY('Venus', 'Mars', 'Jupiter', 'Saturn'),
            'correctAnswer', 1
        )
    )
);
*/

-- ============================================
-- VERIFY TABLES
-- ============================================
-- Tables'ni tekshirish
SHOW TABLES;

-- Har bir table strukturasini ko'rish
DESCRIBE users;
DESCRIBE quizzes;
DESCRIBE quiz_history;
DESCRIBE game_sessions;

-- ============================================
-- SUCCESS MESSAGE
-- ============================================
SELECT 
    '✅ SUCCESS!' AS status,
    'Database tables yaratildi!' AS message,
    COUNT(*) AS total_tables
FROM information_schema.tables 
WHERE table_schema = 'quiz_db';

-- ============================================
-- USEFUL QUERIES
-- ============================================

-- Barcha users'ni ko'rish
-- SELECT * FROM users;

-- Barcha quizzes'ni ko'rish
-- SELECT q.*, u.nickname as creator FROM quizzes q JOIN users u ON q.creator_id = u.id;

-- User tarixi
-- SELECT 
--     h.*,
--     q.title as quiz_title,
--     u.nickname as player
-- FROM quiz_history h
-- JOIN quizzes q ON h.quiz_id = q.id
-- JOIN users u ON h.user_id = u.id
-- ORDER BY h.completed_at DESC;

-- Active game sessions
-- SELECT 
--     s.*,
--     q.title as quiz_title,
--     u.nickname as host
-- FROM game_sessions s
-- JOIN quizzes q ON s.quiz_id = q.id
-- JOIN users u ON s.host_id = u.id
-- WHERE s.status != 'finished';