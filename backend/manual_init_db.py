import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import yaml
from dotenv import load_dotenv

# Load config
def load_config():
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

config = load_config()
db_config = config.get("database", {})

# Load env vars
load_dotenv()

print("Configuration:")
print(f"  Host: {db_config.get('host') or os.getenv('DB_HOST')}")
print(f"  Port: {db_config.get('port') or os.getenv('DB_PORT', 5432)}")
print(f"  User: {db_config.get('user') or os.getenv('DB_USER')}")
print(f"  DB Name: {db_config.get('name') or db_config.get('dbname') or os.getenv('DB_NAME')}")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=db_config.get("user") or os.getenv("DB_USER"),
    password=db_config.get("password") or os.getenv("DB_PASSWORD"),
    host=db_config.get("host") or os.getenv("DB_HOST"),
    port=int(db_config.get("port") or os.getenv("DB_PORT", 5432)),
    database=db_config.get("name") or db_config.get('dbname') or os.getenv("DB_NAME"),
)

def init_db():
    print(f"\nConnecting to database at {DATABASE_URL.render_as_string(hide_password=True)}...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("✅ Connection successful!")
            
            # 1. Create Users Table
            print("\nStep 1: Creating users table...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        hashed_password VARCHAR(255) NOT NULL,
                        role VARCHAR(20) NOT NULL
                    )
                """))
                conn.commit()
                print("✅ Users table created/verified.")
            except Exception as e:
                print(f"❌ Failed to create users table: {e}")

            # 2. Create other tables
            print("\nStep 2: Creating core tables...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS chat_logs (
                        id SERIAL PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT,
                        feedback VARCHAR(20),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                try:
                    conn.execute(text("ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS username VARCHAR(50)"))
                    conn.execute(text("ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS image_path VARCHAR(512)"))
                    conn.execute(text("ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'normal'"))
                    conn.execute(text("ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS sources JSONB"))
                except Exception as e:
                    print(f"  - Migration note: {e}")

                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS learned_qa (
                        id SERIAL PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS question_history (
                        id SERIAL PRIMARY KEY,
                        question TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS uploaded_files (
                        id SERIAL PRIMARY KEY,
                        filename VARCHAR(255) NOT NULL,
                        file_path VARCHAR(512) NOT NULL,
                        uploader VARCHAR(50) NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                print("✅ Core tables created/verified.")
            except Exception as e:
                print(f"❌ Failed to create core tables: {e}")

            # 3. Vector Extension & Documents
            print("\nStep 3: Enabling pgvector and creating documents table...")
            try:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
                print("  - Vector extension enabled.")
                
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id SERIAL PRIMARY KEY,
                        content TEXT,
                        metadata JSONB,
                        embedding vector(1024)
                    )
                """))
                conn.commit()
                print("✅ Documents table created/verified.")
            except Exception as e:
                print(f"⚠️ Warning: Vector extension or documents table creation failed. RAG features will be unavailable.")
                print(f"  Error details: {e}")

            # 4. Seed Users
            print("\nStep 4: Seeding default users...")
            # Simple hash for demo purposes or use passlib if available
            try:
                from passlib.context import CryptContext
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                get_password_hash = pwd_context.hash
            except ImportError:
                print("  - passlib not found, using placeholder hash.")
                get_password_hash = lambda p: f"hashed_{p}"

            try:
                result = conn.execute(text("SELECT username FROM users WHERE username = 'admin'")).fetchone()
                if not result:
                    conn.execute(text("INSERT INTO users (username, hashed_password, role) VALUES ('admin', :p, 'admin')"), 
                                {"p": get_password_hash("admin123")})
                    print("  - Created admin user.")
                
                result = conn.execute(text("SELECT username FROM users WHERE username = 'user'")).fetchone()
                if not result:
                    conn.execute(text("INSERT INTO users (username, hashed_password, role) VALUES ('user', :p, 'user')"), 
                                {"p": get_password_hash("user123")})
                    print("  - Created normal user.")
                conn.commit()
                print("✅ User seeding completed.")
            except Exception as e:
                 print(f"❌ User seeding failed: {e}")

    except Exception as e:
        print(f"\n❌ Critical Error: Could not connect to database or initialize: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
