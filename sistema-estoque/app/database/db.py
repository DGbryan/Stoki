from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Caminho absoluto para fallback local
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'estoque.db')}"

# Obtém a string de conexão direta do banco PostgreSQL do Supabase
DATABASE_URL = os.getenv("SUPABASE_DB_URL", os.getenv("DB_URL", DEFAULT_DB_URL))

# O SQLAlchemy exige que a URL comece com postgresql:// e não apenas postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Argumentos de conexão (check_same_thread é apenas para SQLite)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
