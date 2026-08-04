from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Colis, Adresse, User
from app.schemas import ColisCreate, ColisRead, ColisWithAdresse
from app.services.dependencies import get_current_user


router = APIRouter(prefix="/colis", tags=["colis"])


@router.post("", response_model=ColisRead, status_code=status.HTTP_201_CREATED)
def create_colis(
    payload: ColisCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Enregistre un nouveau colis. Le statut initial est en_attente."""

    existing = session.exec(
        select(Colis).where(Colis.code_barres == payload.code_barres)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Un colis avec le code-barres {payload.code_barres} existe deja",
        )

    colis = Colis(
        code_barres=payload.code_barres,
        telephone=payload.telephone,
        created_by_id=current_user.id,
    )
    session.add(colis)
    session.commit()
    session.refresh(colis)
    return colis


@router.get("", response_model=List[ColisRead])
def list_colis(session: Session = Depends(get_session)):
    """Liste tous les colis, du plus recent au plus ancien."""
    result = session.exec(select(Colis).order_by(Colis.created_at.desc())).all()
    return result


@router.get("/{colis_id}", response_model=ColisWithAdresse)
def get_colis(colis_id: int, session: Session = Depends(get_session)):
    """Recupere un colis par son id, avec son adresse si elle a ete collectee."""
    colis = session.get(Colis, colis_id)
    if not colis:
        raise HTTPException(status_code=404, detail="Colis introuvable")

    adresse = session.exec(
        select(Adresse).where(Adresse.colis_id == colis_id)
    ).first()

    return ColisWithAdresse(
        id=colis.id,
        code_barres=colis.code_barres,
        telephone=colis.telephone,
        statut=colis.statut,
        sent_at=colis.sent_at,
        reminder_sent_at=colis.reminder_sent_at,
        created_at=colis.created_at,
        adresse=adresse,
    )