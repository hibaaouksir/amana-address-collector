"""
Factory pour instancier le bon AddressExtractor selon la configuration.

Providers disponibles :
- "mock"   : mock pour dev/tests sans consommer de quota
- "gemini" : Google Gemini (recommande pour ton stage)
"""
import os
from dotenv import load_dotenv

from app.services.address_extractor import AddressExtractor

load_dotenv()


def get_address_extractor() -> AddressExtractor:
    """Retourne l instance AddressExtractor configuree via ADDRESS_EXTRACTOR_PROVIDER."""
    provider = os.getenv("ADDRESS_EXTRACTOR_PROVIDER", "mock").lower()

    if provider == "gemini":
        from app.services.gemini_address_extractor import GeminiAddressExtractor
        return GeminiAddressExtractor()
    elif provider == "mock":
        from app.services.mock_address_extractor import MockAddressExtractor
        return MockAddressExtractor()
    else:
        raise ValueError(
            f"ADDRESS_EXTRACTOR_PROVIDER={provider} inconnu. Valeurs valides : mock, gemini"
        )