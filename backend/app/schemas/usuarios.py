from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class UsuarioBase(BaseModel):
    username: str = Field(..., examples=["mozo1"])
    nombre: str
    rol: str = Field(..., examples=["mozo", "cocina", "caja", "admin"])
    activo: bool = True
    cajas_ids: Optional[List[int]] = Field(default=None, description="IDs de cajas asignadas")


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)
    pin: str = Field(..., min_length=4, max_length=6)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None
    cajas_ids: Optional[List[int]] = None
    password: Optional[str] = Field(default=None, min_length=6)
    pin: Optional[str] = Field(default=None, min_length=4, max_length=6)


class UsuarioPublic(ORMModel):
    id: int
    username_lower: str
    nombre: str
    rol: str
    activo: bool
    cajas_asignadas: List[int] = Field(default_factory=list)
