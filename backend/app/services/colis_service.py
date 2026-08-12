"""
Service metier pour la gestion des colis.
Contient la logique : creer un colis + envoyer la demande WhatsApp.
"""
from datetime import datetime, timezone
from sqlmodel import Session

from app.models import Colis, User
from app.services.whatsapp_factory import get_whatsapp_sender


MESSAGE_TEMPLATE = (
    "Bonjour ! Nous avons un colis a vous livrer de la part d Amana - Barid Al-Maghrib. "
    "Pour organiser la livraison, merci de repondre a ce message en nous partageant "
    "votre adresse complete ou votre localisation.\n\n"
    "Merci."
)


def create_colis_and_send_whatsapp(
    session: Session,
    code_barres: str,
    telephone: str,
    created_by: User,
) -> tuple[Colis, dict]:
    """Cree un colis en base et envoie le message WhatsApp au destinataire.

    Args:
        session: Session SQLModel
        code_barres: Code-barres du colis
        telephone: Numero du destinataire (format +212...)
        created_by: Employe qui enregistre le colis

    Returns:
        (colis, whatsapp_result) : le colis persiste + le resultat de l envoi WhatsApp
    """

    # 1. Creer le colis en base
    colis = Colis(
        code_barres=code_barres,
        telephone=telephone,
        created_by_id=created_by.id,
        statut="en_attente",
    )
    session.add(colis)
    session.commit()
    session.refresh(colis)

    # 2. Envoyer le message WhatsApp
    sender = get_whatsapp_sender()
    result = sender.send_message(to_phone=telephone, message=MESSAGE_TEMPLATE)

    # 3. Mettre a jour le statut selon le resultat
    if result.get("success"):
        colis.statut = "envoye"
        colis.sent_at = datetime.now(timezone.utc)
    else:
        colis.statut = "echec_envoi"

    session.add(colis)
    session.commit()
    session.refresh(colis)

    return colis, result