from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.core.security import get_password_hash
from app.models.models import Caja, RoleEnum, Usuario
from app.schemas.common import Paginated
from app.schemas.usuarios import UsuarioCreate, UsuarioPublic, UsuarioUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=Paginated[UsuarioPublic],
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def list_usuarios(db: Session = Depends(get_db), page: int = 1, size: int = 50):
    query = db.query(Usuario)
    total = query.count()
    usuarios = query.offset((page - 1) * size).limit(size).all()
    response_items: List[UsuarioPublic] = []
    for user in usuarios:
        response_items.append(
            UsuarioPublic(
                id=user.id,
                username_lower=user.username_lower,
                nombre=user.nombre,
                rol=user.rol.value,
                activo=user.activo,
                cajas_asignadas=[c.id for c in user.cajas_asignadas],
            )
        )
    return Paginated[UsuarioPublic](items=response_items, total=total, page=page, size=size)


@router.post(
    "/",
    response_model=UsuarioPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def create_usuario(data: UsuarioCreate, db: Session = Depends(get_db)) -> UsuarioPublic:
    username_lower = data.username.lower()
    if db.query(Usuario).filter(Usuario.username_lower == username_lower).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario duplicado")

    usuario = Usuario(
        username_lower=username_lower,
        nombre=data.nombre,
        rol=RoleEnum(data.rol),
        password_hash=get_password_hash(data.password),
        pin_hash=get_password_hash(data.pin),
    )

    if data.cajas_ids:
        cajas = db.query(Caja).filter(Caja.id.in_(data.cajas_ids)).all()
        usuario.cajas_asignadas = cajas

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return UsuarioPublic(
        id=usuario.id,
        username_lower=usuario.username_lower,
        nombre=usuario.nombre,
        rol=usuario.rol.value,
        activo=usuario.activo,
        cajas_asignadas=[c.id for c in usuario.cajas_asignadas],
    )


@router.put(
    "/{usuario_id}",
    response_model=UsuarioPublic,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def update_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)) -> UsuarioPublic:
    usuario: Usuario | None = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if data.nombre is not None:
        usuario.nombre = data.nombre
    if data.rol is not None:
        usuario.rol = RoleEnum(data.rol)
    if data.activo is not None:
        usuario.activo = data.activo
    if data.password:
        usuario.password_hash = get_password_hash(data.password)
    if data.pin:
        usuario.pin_hash = get_password_hash(data.pin)
    if data.cajas_ids is not None:
        cajas = db.query(Caja).filter(Caja.id.in_(data.cajas_ids)).all()
        usuario.cajas_asignadas = cajas

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return UsuarioPublic(
        id=usuario.id,
        username_lower=usuario.username_lower,
        nombre=usuario.nombre,
        rol=usuario.rol.value,
        activo=usuario.activo,
        cajas_asignadas=[c.id for c in usuario.cajas_asignadas],
    )


@router.get("/me", response_model=UsuarioPublic, dependencies=[Depends(get_current_user)])
def get_me(current_user: Usuario = Depends(get_current_user)) -> UsuarioPublic:
    return UsuarioPublic(
        id=current_user.id,
        username_lower=current_user.username_lower,
        nombre=current_user.nombre,
        rol=current_user.rol.value,
        activo=current_user.activo,
        cajas_asignadas=[c.id for c in current_user.cajas_asignadas],
    )
