from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """Un employe Amana qui utilise l application."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Colis(SQLModel, table=True):
    """Un colis enregistre par un employe, en attente d adresse."""

    id: Optional[int] = Field(default=None, primary_key=True)
    code_barres: str = Field(unique=True, index=True)
    telephone: str
    statut: str = Field(default="en_attente")

    sent_at: Optional[datetime] = None
    reminder_sent_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Adresse(SQLModel, table=True):
    """L adresse collectee via WhatsApp pour un colis."""

    id: Optional[int] = Field(default=None, primary_key=True)
    colis_id: int = Field(foreign_key="colis.id", unique=True)

    ligne1: Optional[str] = None
    ville: Optional[str] = None
    code_postal: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    source: str
    raw_response: str

    extracted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
