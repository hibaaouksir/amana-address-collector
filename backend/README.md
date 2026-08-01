# Amana Address Collector

Application interne Barid Al-Maghrib — collecte automatique des adresses de destinataires via WhatsApp lorsqu'un colis arrive sans adresse.

## Démarrage

    cd backend
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Copy-Item .env.example .env
    fastapi dev app/main.py

Documentation Swagger : http://localhost:8000/docs
