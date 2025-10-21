from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.security import create_token, decode_token, verify_password
from app.models.models import Usuario
from app.schemas.auth import CurrentUser, LoginRequest, RefreshRequest, Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db=Depends(get_db)) -> Token:
    username = data.username.lower()
    user: Usuario | None = db.query(Usuario).filter(Usuario.username_lower == username).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    if not user.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

    access_token = create_token(user.username_lower)
    refresh_token = create_token(
        user.username_lower,
        expires_delta=timedelta(minutes=settings.refresh_token_expire_minutes),
        token_type="refresh",
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
def refresh(data: RefreshRequest) -> Token:
    try:
        payload = decode_token(data.refresh_token)
    except ValueError as exc:  # pragma: no cover - FastAPI maneja el error
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido") from exc

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    access_token = create_token(username)
    new_refresh = create_token(
        username,
        expires_delta=timedelta(minutes=settings.refresh_token_expire_minutes),
        token_type="refresh",
    )
    return Token(access_token=access_token, refresh_token=new_refresh)


@router.get("/me", response_model=CurrentUser)
def read_me(current_user: Usuario = Depends(get_current_user)) -> CurrentUser:
    return CurrentUser(
        id=current_user.id,
        username=current_user.username_lower,
        nombre=current_user.nombre,
        rol=current_user.rol.value,
        activo=current_user.activo,
    )
