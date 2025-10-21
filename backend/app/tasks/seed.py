"""Script simple para poblar datos demo en la base local."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.models import Caja, CategoriaProducto, Cliente, RoleEnum, Usuario


def seed_base(session: Session) -> None:
    if session.query(Usuario).count():
        return

    admin = Usuario(
        username_lower="admin",
        nombre="Administrador",
        rol=RoleEnum.ADMIN,
        password_hash=get_password_hash("admin123"),
        pin_hash=get_password_hash("1234"),
    )
    mozo = Usuario(
        username_lower="mozo1",
        nombre="Mozo Demo",
        rol=RoleEnum.MOZO,
        password_hash=get_password_hash("mozo123"),
        pin_hash=get_password_hash("5678"),
    )
    caja = Caja(nombre="Caja Principal", activo=True)
    categoria_bebidas = CategoriaProducto(nombre="Bebidas")
    cliente = Cliente(nombre="Consumidor Final", telefono="", email=None, descuento_pct=None)

    session.add_all([admin, mozo, caja, categoria_bebidas, cliente])
    session.commit()

    caja.usuarios.append(admin)
    session.add(caja)
    session.commit()


if __name__ == "__main__":  # pragma: no cover
    with SessionLocal() as session:
        seed_base(session)
        print("Datos demo cargados", datetime.utcnow())
