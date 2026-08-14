"""
Interface abstraite pour extraire une adresse a partir d un texte libre.

Toute implementation (Gemini, Claude, OpenAI, Mock) doit heriter de cette classe
et implementer la methode extract.
"""
from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, Field


class ExtractedAddress(BaseModel):
    """Structure retournee par l extraction IA d une adresse."""

    ligne1: Optional[str] = Field(None, description="Rue, numero, batiment, appartement")
    ville: Optional[str] = Field(None, description="Ville")
    code_postal: Optional[str] = Field(None, description="Code postal si mentionne")
    points_repere: Optional[str] = Field(None, description="Reperes utiles pour la livraison")
    confiance: str = Field("moyenne", description="haute, moyenne, ou basse")
    raw_response: str = Field(..., description="Reponse brute du destinataire")


class AddressExtractor(ABC):
    """Interface pour extraire une adresse structuree d un message texte."""

    @abstractmethod
    def extract(self, message: str) -> ExtractedAddress:
        """Extrait une adresse structuree du message.

        Args:
            message: Le texte brut envoye par le destinataire via WhatsApp

        Returns:
            ExtractedAddress avec les composantes structurees + niveau de confiance
        """
        pass