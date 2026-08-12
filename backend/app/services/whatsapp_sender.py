"""
Interface commune pour tous les providers WhatsApp.
Permet de brancher n importe quel provider (pywhatkit, Meta, Twilio, Vonage) 
sans changer le code metier.
"""
from abc import ABC, abstractmethod
from typing import Optional


class WhatsAppSender(ABC):
    """Interface abstraite pour envoyer des messages WhatsApp.
    
    Toute implementation concrete doit heriter de cette classe et implementer
    la methode send_message.
    """

    @abstractmethod
    def send_message(self, to_phone: str, message: str) -> dict:
        """Envoie un message WhatsApp a un numero.

        Args:
            to_phone: Numero destinataire au format international, ex: +212612345678
            message: Contenu texte du message

        Returns:
            dict avec au minimum :
                - success (bool): True si envoye
                - message_id (str, optional): identifiant du message chez le provider
                - error (str, optional): message d erreur si echec
        """
        pass