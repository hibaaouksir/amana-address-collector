from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models import User
from app.schemas import UserRegister, UserRead, UserLogin, TokenResponse
from app.services.security import hash_password, verify_password, create_access_token
from app.services.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, session: Session = Depends(get_session)):
    """Cree un nouveau compte employe."""

    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte avec cet email existe deja",
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, session: Session = Depends(get_session)):
    """Connecte un employe avec JSON et renvoie un token JWT.

    Endpoint principal pour le frontend qui envoie du JSON.
    """
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )

    access_token = create_access_token(user_id=user.id)
    return TokenResponse(
        access_token=access_token,
        user=UserRead(id=user.id, email=user.email, name=user.name),
    )


@router.post("/token", response_model=TokenResponse)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """Endpoint compatible OAuth2 pour Swagger UI.

    Utilise le format form-urlencoded avec 'username' au lieu de 'email'.
    Meme logique que /auth/login mais pour le bouton Authorize de Swagger.
    """
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_id=user.id)
    return TokenResponse(
        access_token=access_token,
        user=UserRead(id=user.id, email=user.email, name=user.name),
    )


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    """Renvoie l employe actuellement connecte."""
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
    )