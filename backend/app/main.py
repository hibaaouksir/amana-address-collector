from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Amana Address Collector",
    description="Collecte automatique d'adresses via WhatsApp",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "amana-address-collector"}
