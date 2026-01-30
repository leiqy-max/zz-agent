-- 1. Enable pgvector extension (requires superuser or allowlist)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- 3. Create chat_logs table
CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    question TEXT NOT NULL,
    answer TEXT,
    feedback VARCHAR(20),
    image_path VARCHAR(512),
    status VARCHAR(20) DEFAULT 'normal',
    sources JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create learned_qa table
CREATE TABLE IF NOT EXISTS learned_qa (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Create question_history table
CREATE TABLE IF NOT EXISTS question_history (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Create uploaded_files table
CREATE TABLE IF NOT EXISTS uploaded_files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    uploader VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Create documents table (for RAG)
-- Note: The vector dimension is set to 1024 for BAAI/bge-m3. 
-- If you use a different model, change 1024 to the correct dimension (e.g., 1536 for OpenAI).
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding vector(1024)
);

-- 8. Create index for faster vector search (optional but recommended)
-- CREATE INDEX ON documents USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);

-- 9. Insert default admin user (password: admin123)
-- Hash generated using bcrypt
INSERT INTO users (username, hashed_password, role) 
VALUES ('admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxwKc.6IymCs7CN52au9gm.C8O.V.', 'admin')
ON CONFLICT (username) DO NOTHING;

-- 10. Insert default normal user (password: user123)
INSERT INTO users (username, hashed_password, role) 
VALUES ('user', '$2b$12$8U2rUAW8mmXnEX3w5ux2TuHnuZVPc9yAGYoUpGkT4BhgX8XqoVvay', 'user')
ON CONFLICT (username) DO NOTHING;
