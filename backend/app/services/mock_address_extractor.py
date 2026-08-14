"""
Implementation MOCK pour tester la structure sans appeler l API Gemini.

Detecte quelques mots-cles marocains (Rabat, Casablanca, etc.) et retourne 
une adresse factice mais coherente. Utile pour le developpement sans consommer 
le quota API.
"""
from app.services.address_extractor import AddressExtractor, ExtractedAddress


class MockAddressExtractor(AddressExtractor):
    """Extracteur mock avec detection basique de mots-cles."""

    def extract(self, message: str) -> ExtractedAddress:
        """Simule une extraction en detectant des mots-cles."""
        message_lower = message.lower()

        # Detecter la ville si mentionnee
        ville = None
        for v in ["rabat", "casablanca", "casa", "marrakech", "fes", "fez", "tanger", "agadir", "meknes"]:
            if v in message_lower:
                ville = v.capitalize()
                break

        return ExtractedAddress(
            ligne1=f"[MOCK] Adresse extraite du message : {message[:80]}",
            ville=ville or "Rabat",
            code_postal=None,
            points_repere="[MOCK] Utilise MockAddressExtractor - pas de vraie extraction IA",
            confiance="basse",
            raw_response=message,
        )