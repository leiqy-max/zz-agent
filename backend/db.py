import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from config_loader import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Priority: Config file > Env vars
db_config = config.db

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=db_config.get("user") or os.getenv("DB_USER"),
    password=db_config.get("password") or os.getenv("DB_PASSWORD"),
    host=db_config.get("host") or os.getenv("DB_HOST"),
    port=int(db_config.get("port") or os.getenv("DB_PORT", 5432)),
    database=db_config.get("name") or db_config.get("dbname") or os.getenv("DB_NAME"),
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
