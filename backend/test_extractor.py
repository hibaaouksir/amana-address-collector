"""Test isole de l extracteur d adresse (mock)."""
from app.services.address_extractor_factory import get_address_extractor


TEST_MESSAGES = [
    "Rue Ibn Sina, residence Al Andalous, immeuble B appartement 12, Agdal Rabat",
    "salam je suis a hay salam bloc 5 3ma khadija bghit tjib li colis",
    "Face a la mosquee verte, a cote de la pharmacie, 2eme etage, Casablanca",
    "Bonjour, l adresse est boulevard Mohammed VI, immeuble 45, Marrakech",
]


def main():
    extractor = get_address_extractor()
    print(f"Extractor utilise : {type(extractor).__name__}")
    print("=" * 70)

    for i, msg in enumerate(TEST_MESSAGES, 1):
        print(f"\nMessage {i} : {msg[:60]}...")
        result = extractor.extract(msg)
        print(f"  ligne1        : {result.ligne1}")
        print(f"  ville         : {result.ville}")
        print(f"  code_postal   : {result.code_postal}")
        print(f"  points_repere : {result.points_repere}")
        print(f"  confiance     : {result.confiance}")


if __name__ == "__main__":
    main()