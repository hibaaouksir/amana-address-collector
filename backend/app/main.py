from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from app.database import create_db_and_tables
from app import models  # noqa: F401  -- necessaire pour enregistrer les modeles

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au demarrage : creer les tables si elles n'existent pas
    create_db_and_tables()
    yield
    # A l'arret : rien pour l'instant


app = FastAPI(
    title="Amana Address Collector",
    description="Collecte automatique d'adresses via WhatsApp",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "amana-address-collector"}