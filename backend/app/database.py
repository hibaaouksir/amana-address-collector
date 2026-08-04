import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL manquant dans .env")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Cree toutes les tables definies dans models.py si elles n existent pas."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Fournit une session DB pour les endpoints FastAPI."""
    with Session(engine) as session:
        yield session
