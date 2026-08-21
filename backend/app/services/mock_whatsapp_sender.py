"""
Implementation MOCK pour le developpement et la demonstration.

Simule l envoi WhatsApp en loggant dans le terminal, sans appel externe.
Aucune dependance reseau, aucun risque de bug, envoi instantane.
"""
from datetime import datetime

from app.services.whatsapp_sender import WhatsAppSender


class MockWhatsAppSender(WhatsAppSender):
    """Provider mock qui simule l envoi WhatsApp sans rien envoyer."""

    def send_message(self, to_phone: str, message: str) -> dict:
        """Simule un envoi en affichant le message dans les logs serveur."""
        timestamp = datetime.now().isoformat()

        print()
        print("=" * 70)
        print("[MOCK WHATSAPP SIMULATION]")
        print(f"Timestamp : {timestamp}")
        print(f"To        : {to_phone}")
        print(f"Message   :")
        for line in message.split("\n"):
            print(f"            {line}")
        print("=" * 70)
        print()

        return {
            "success": True,
            "message_id": f"mock-{timestamp}",
            "provider": "mock",
        }