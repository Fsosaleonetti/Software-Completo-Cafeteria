from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.schemas.common import ORMModel


class ClienteBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    descuento_pct: Optional[float] = None


class ClienteCreate(ClienteBase):
    cta_corriente_saldo: Decimal = Decimal("0")


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    descuento_pct: Optional[float] = None
    cta_corriente_saldo: Optional[Decimal] = None


class ClientePublic(ORMModel):
    id: int
    nombre: str
    telefono: Optional[str]
    email: Optional[str]
    descuento_pct: Optional[float]
    cta_corriente_saldo: Decimal
