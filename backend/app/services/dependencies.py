from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.database import get_session
from app.models import User
from app.services.security import decode_access_token


# OAuth2PasswordBearer indique a FastAPI ou trouver le token :
# dans l en-tete Authorization: Bearer <token>
# tokenUrl est utilise par Swagger pour son bouton Authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Recupere l utilisateur courant a partir du token JWT.
    Renvoie 401 si le token est absent, invalide, ou si l utilisateur n existe pas."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expire",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user