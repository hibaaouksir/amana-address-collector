"""
Factory pour instancier le bon WhatsAppSender selon la configuration.

Providers disponibles :
- "mock"      : simulation (dev/demo, aucun envoi reel) [RECOMMANDE POUR DEV]
- "pywhatkit" : envoi reel via WhatsApp Web (fragile, dev uniquement)
- "meta"      : API officielle WhatsApp Business (production Barid)
"""
import os
from dotenv import load_dotenv

from app.services.whatsapp_sender import WhatsAppSender

load_dotenv()


def get_whatsapp_sender() -> WhatsAppSender:
    """Retourne l instance WhatsAppSender configuree via WHATSAPP_PROVIDER."""
    provider = os.getenv("WHATSAPP_PROVIDER", "mock").lower()

    if provider == "meta":
        from app.services.meta_whatsapp_sender import MetaWhatsAppSender
        return MetaWhatsAppSender()
    elif provider == "pywhatkit":
        from app.services.pywhatkit_sender import PywhatkitSender
        return PywhatkitSender()
    elif provider == "mock":
        from app.services.mock_whatsapp_sender import MockWhatsAppSender
        return MockWhatsAppSender()
    else:
        raise ValueError(
            f"WHATSAPP_PROVIDER={provider} inconnu. Valeurs valides : mock, pywhatkit, meta"
        )