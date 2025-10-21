from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.models import Cliente, RoleEnum
from app.schemas.clientes import ClienteCreate, ClientePublic, ClienteUpdate
from app.schemas.common import Paginated

router = APIRouter(dependencies=[Depends(require_roles(RoleEnum.ADMIN, RoleEnum.CAJA, RoleEnum.MOZO))])


@router.get("/", response_model=Paginated[ClientePublic])
def list_clientes(db: Session = Depends(get_db), page: int = 1, size: int = 50):
    query = db.query(Cliente)
    total = query.count()
    clientes = query.offset((page - 1) * size).limit(size).all()
    items: List[ClientePublic] = [ClientePublic.model_validate(cliente) for cliente in clientes]
    return Paginated[ClientePublic](items=items, total=total, page=page, size=size)


@router.post("/", response_model=ClientePublic, status_code=status.HTTP_201_CREATED)
def create_cliente(data: ClienteCreate, db: Session = Depends(get_db)) -> ClientePublic:
    cliente = Cliente(**data.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return ClientePublic.model_validate(cliente)


@router.get("/{cliente_id}", response_model=ClientePublic)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)) -> ClientePublic:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return ClientePublic.model_validate(cliente)


@router.put("/{cliente_id}", response_model=ClientePublic)
def update_cliente(cliente_id: int, data: ClienteUpdate, db: Session = Depends(get_db)) -> ClientePublic:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cliente, field, value)

    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return ClientePublic.model_validate(cliente)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)) -> None:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()


@router.post("/import", status_code=status.HTTP_202_ACCEPTED)
def import_clientes() -> dict[str, str]:
    return {"detail": "Importación asíncrona pendiente de implementación"}
