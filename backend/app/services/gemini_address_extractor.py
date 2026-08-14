"""
Implementation AddressExtractor utilisant Google Gemini API.

Utilise le mode structured output (JSON schema) pour garantir une reponse
strictement typee, sans hallucination de format.

Modele utilise : gemini-2.5-flash-lite (rapide, economique, dans le free tier).
"""
import json
import os
from google import genai
from google.genai import types

from app.services.address_extractor import AddressExtractor, ExtractedAddress


# Prompt system : explique a l IA son role, le contexte marocain, et les regles
SYSTEM_PROMPT = """Tu es un extracteur d'adresses postales marocaines. Tu recois un message texte envoye
par le destinataire d'un colis via WhatsApp, en reponse a une demande d'adresse.

Ton role : analyser le message et extraire une adresse structuree.

Contexte important :
- Les messages peuvent etre en francais, arabe, ou darija latinisee (arabe marocain ecrit en caracteres latins)
- Les adresses marocaines suivent souvent le format : Rue/Boulevard + numero + immeuble + appartement + quartier + ville
- Certains messages sont informels : "chez X", "face a la mosquee", "a cote de la pharmacie"
- Certains messages contiennent des points de repere plutot qu'une adresse formelle
- Les villes principales : Casablanca (Casa), Rabat, Marrakech, Fes, Tanger, Agadir, Meknes, Oujda, Kenitra
- Les codes postaux marocains sont sur 5 chiffres (ex: 10090 pour Agdal Rabat)

Regles d'extraction :
1. ligne1 : la partie principale de l'adresse (rue, numero, immeuble, apt). Si informel, mets une description utile pour le livreur.
2. ville : nom de la ville detecte ou deductible. Ecris-la correctement (Casablanca et non Casa).
3. code_postal : uniquement si mentionne explicitement dans le message. Sinon null.
4. points_repere : reperes utiles pour le livreur (mosquee, pharmacie, ecole, personne...). Si aucun, null.
5. confiance :
   - "haute" : adresse claire et complete (rue + ville + numero identifie)
   - "moyenne" : adresse comprehensible mais partielle
   - "basse" : message vague, ambigu, ou hors sujet

Si le message ne contient AUCUNE information d'adresse (ex: "c'est quand la livraison?"),
retourne tout en null avec confiance "basse" et points_repere = "Message ne contient pas d'adresse".
"""


class GeminiAddressExtractor(AddressExtractor):
    """Extracteur d adresse utilisant Google Gemini avec structured output."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY manquant dans .env")

        # Client Gemini
        self.client = genai.Client(api_key=api_key)

        # Modele actif en 2026 : gemini-2.5-flash-lite est le plus economique
        # et fonctionne parfaitement pour de l extraction courte structuree.
        # Alternatives : gemini-2.5-flash, gemini-3.5-flash-lite, gemini-3.6-flash
        self.model_name = "gemini-3.5-flash-lite"

    def extract(self, message: str) -> ExtractedAddress:
        """Extrait une adresse structuree via Gemini."""

        try:
            # Appel a l API Gemini avec structured output
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"Message a analyser :\n\n{message}",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema={
                        "type": "object",
                        "properties": {
                            "ligne1": {"type": "string", "nullable": True},
                            "ville": {"type": "string", "nullable": True},
                            "code_postal": {"type": "string", "nullable": True},
                            "points_repere": {"type": "string", "nullable": True},
                            "confiance": {
                                "type": "string",
                                "enum": ["haute", "moyenne", "basse"],
                            },
                        },
                        "required": ["confiance"],
                    },
                ),
            )

            # Gemini retourne un JSON en string, on le parse
            data = json.loads(response.text)

            return ExtractedAddress(
                ligne1=data.get("ligne1"),
                ville=data.get("ville"),
                code_postal=data.get("code_postal"),
                points_repere=data.get("points_repere"),
                confiance=data.get("confiance", "moyenne"),
                raw_response=message,
            )

        except Exception as e:
            # En cas d erreur API, on retourne une adresse vide avec confiance basse
            # plutot que de crasher toute la requete
            return ExtractedAddress(
                ligne1=None,
                ville=None,
                code_postal=None,
                points_repere=f"[ERREUR IA] {str(e)[:200]}",
                confiance="basse",
                raw_response=message,
            )