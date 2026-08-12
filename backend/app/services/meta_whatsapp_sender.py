"""
Implementation WhatsAppSender utilisant l API officielle WhatsApp Business Cloud (Meta).

C EST L IMPLEMENTATION POUR LA PRODUCTION.
Barid Al-Maghrib doit :
1. Creer un compte Meta Business (business.facebook.com)
2. Verifier son identite d entreprise avec Meta
3. Obtenir un numero WhatsApp Business dedie
4. Recuperer un Access Token permanent et son Phone Number ID
5. Mettre ces valeurs dans .env :
   WHATSAPP_META_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxx...
   WHATSAPP_META_PHONE_NUMBER_ID=123456789012345
6. Changer WHATSAPP_PROVIDER=meta dans .env
7. Redemarrer l application

Aucune autre modification de code n est necessaire.
"""
import os
import requests

from app.services.whatsapp_sender import WhatsAppSender


class MetaWhatsAppSender(WhatsAppSender):
    """Envoi WhatsApp via l API officielle Meta WhatsApp Business Cloud."""

    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_META_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_META_PHONE_NUMBER_ID")

        if not self.access_token or not self.phone_number_id:
            raise RuntimeError(
                "MetaWhatsAppSender necessite WHATSAPP_META_ACCESS_TOKEN "
                "et WHATSAPP_META_PHONE_NUMBER_ID dans .env"
            )

        self.api_url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}/messages"

    def send_message(self, to_phone: str, message: str) -> dict:
        """Envoie un message texte via l API Meta.

        Note : en production reelle, il faut utiliser des message templates
        pre-approuves par Meta pour initier une conversation avec un numero.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        to_phone_clean = to_phone.lstrip("+")

        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone_clean,
            "type": "text",
            "text": {
                "body": message,
            },
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            message_id = data.get("messages", [{}])[0].get("id", "unknown")

            return {
                "success": True,
                "message_id": message_id,
                "provider": "meta",
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "error": f"Erreur HTTP {response.status_code}: {response.text}",
                "provider": "meta",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "meta",
            }