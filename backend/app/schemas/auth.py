from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    type: str


class LoginRequest(BaseModel):
    username: str = Field(..., examples=["mozo1"])
    password: str = Field(..., examples=["secreto"])


class RefreshRequest(BaseModel):
    refresh_token: str


class CurrentUser(BaseModel):
    id: int
    username: str
    nombre: str
    rol: str
    activo: bool
    last_login: Optional[datetime] = None
