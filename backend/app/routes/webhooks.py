"""
Routes pour les webhooks WhatsApp (reponses des destinataires).

Pour l instant, un endpoint de simulation manuelle pour tester le flux end-to-end.
En production, Meta enverra les webhooks sur POST /webhooks/whatsapp-reply avec
une structure specifique qu il faudra parser.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
from app.models import Colis, Adresse
from app.schemas import WhatsAppReplySimulation, AdresseRead
from app.services.address_extractor_factory import get_address_extractor


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/whatsapp-reply", response_model=AdresseRead, status_code=status.HTTP_201_CREATED)
def receive_whatsapp_reply(
    payload: WhatsAppReplySimulation,
    session: Session = Depends(get_session),
):
    """Simule la reception d une reponse WhatsApp du destinataire.

    Flow :
    1. Verifie que le colis existe
    2. Extrait l adresse via IA (Gemini)
    3. Enregistre une nouvelle Adresse en base
    4. Met a jour le statut du colis a "adresse_recue"
    """
    # 1. Verifier que le colis existe
    colis = session.get(Colis, payload.colis_id)
    if not colis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Colis {payload.colis_id} introuvable",
        )

    # 2. Extraire l adresse via IA
    extractor = get_address_extractor()
    extracted = extractor.extract(payload.message)

    print(f"[EXTRACTION IA] Colis {payload.colis_id}")
    print(f"  Message brut : {payload.message}")
    print(f"  Extrait      : {extracted.model_dump()}")

    # 3. Enregistrer l adresse
    adresse = Adresse(
        colis_id=payload.colis_id,
        ligne1=extracted.ligne1,
        ville=extracted.ville,
        code_postal=extracted.code_postal,
        latitude=None,   # Sera renseigne si le destinataire partage sa localisation GPS
        longitude=None,
        source="texte",
        raw_response=payload.message,
    )
    session.add(adresse)

    # 4. Mettre a jour le colis
    colis.statut = "adresse_recue"
    session.add(colis)

    session.commit()
    session.refresh(adresse)

    return adresse