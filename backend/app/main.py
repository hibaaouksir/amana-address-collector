from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from app.database import create_db_and_tables
from app import models  # noqa: F401
from app.routes import colis as colis_routes

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Amana Address Collector",
    description="Collecte automatique d'adresses via WhatsApp",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(colis_routes.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "amana-address-collector"}