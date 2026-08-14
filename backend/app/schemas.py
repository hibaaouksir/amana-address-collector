from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


# ===== Schemas pour Colis =====

class ColisCreate(SQLModel):
    """Ce que l employe envoie pour creer un colis."""
    code_barres: str
    telephone: str


class ColisRead(SQLModel):
    """Ce que l API renvoie quand on lit un colis."""
    id: int
    code_barres: str
    telephone: str
    statut: str
    sent_at: Optional[datetime] = None
    reminder_sent_at: Optional[datetime] = None
    created_at: datetime


# ===== Schemas pour Adresse =====

class AdresseRead(SQLModel):
    """Adresse collectee pour un colis (lecture seule pour l instant)."""
    id: int
    colis_id: int
    ligne1: Optional[str] = None
    ville: Optional[str] = None
    code_postal: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: str
    extracted_at: datetime


class ColisWithAdresse(ColisRead):
    """Un colis avec son adresse collectee (si disponible)."""
    adresse: Optional[AdresseRead] = None

class UserLogin(SQLModel):
    """Ce que l'employé envoie pour se connecter."""
    email: str
    password: str


class TokenResponse(SQLModel):
    """Ce que l'API renvoie après une connexion réussie."""
    access_token: str
    token_type: str = "bearer"
    user: UserRead
# ===== Schemas pour Auth =====

class UserRegister(SQLModel):
    """Ce que l'employé envoie pour créer un compte."""
    email: str
    password: str
    name: str


class UserRead(SQLModel):
    """Ce que l'API renvoie pour un utilisateur (jamais le mot de passe !)."""
    id: int
    email: str
    name: str

class WhatsAppReplySimulation(SQLModel):
    """Simule une réponse WhatsApp reçue d'un destinataire."""
    colis_id: int
    message: str