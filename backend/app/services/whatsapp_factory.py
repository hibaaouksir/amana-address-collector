"""
Factory pour instancier le bon WhatsAppSender selon la configuration.

En dev/demo : WHATSAPP_PROVIDER=pywhatkit
En production Barid : WHATSAPP_PROVIDER=meta
"""
import os
from dotenv import load_dotenv

from app.services.whatsapp_sender import WhatsAppSender

load_dotenv()


def get_whatsapp_sender() -> WhatsAppSender:
    """Retourne l instance WhatsAppSender configuree.

    Utilise la variable d environnement WHATSAPP_PROVIDER :
    - "pywhatkit" (defaut) : pour le dev/demo
    - "meta" : pour la production avec l API officielle Meta
    """
    provider = os.getenv("WHATSAPP_PROVIDER", "pywhatkit").lower()

    if provider == "meta":
        from app.services.meta_whatsapp_sender import MetaWhatsAppSender
        return MetaWhatsAppSender()
    elif provider == "pywhatkit":
        from app.services.pywhatkit_sender import PywhatkitSender
        return PywhatkitSender()
    else:
        raise ValueError(
            f"WHATSAPP_PROVIDER={provider} inconnu. Valeurs valides : pywhatkit, meta"
        )