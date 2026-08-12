"""
Script de test isole pour valider l envoi WhatsApp via le service configure.

Utilisation : python test_whatsapp.py
"""
from app.services.whatsapp_factory import get_whatsapp_sender


# ===== CONFIGURATION DU TEST =====
# Remplace par le numero de test qui va recevoir le message
TEST_PHONE = "+212676890412"

TEST_MESSAGE = (
    "Bonjour ! Ceci est un message de test envoye depuis l application "
    "Amana Address Collector. Si vous recevez ce message, l integration "
    "WhatsApp fonctionne correctement."
)
# ==================================


def main():
    print("=" * 60)
    print("Test envoi WhatsApp - Amana Address Collector")
    print("=" * 60)

    # Recupere le sender configure via .env
    sender = get_whatsapp_sender()
    print(f"Provider utilise : {type(sender).__name__}")
    print(f"Destinataire     : {TEST_PHONE}")
    print(f"Message          : {TEST_MESSAGE[:60]}...")
    print()
    print("Envoi en cours... (Chrome va s ouvrir automatiquement)")
    print("Si un QR code apparait, scanne-le avec ton telephone.")
    print()

    result = sender.send_message(to_phone=TEST_PHONE, message=TEST_MESSAGE)

    print("=" * 60)
    if result.get("success"):
        print("SUCCESS : Message envoye avec succes !")
        print(f"Message ID : {result.get('message_id')}")
    else:
        print("ECHEC : L envoi a echoue")
        print(f"Erreur : {result.get('error')}")
    print("=" * 60)


if __name__ == "__main__":
    main()