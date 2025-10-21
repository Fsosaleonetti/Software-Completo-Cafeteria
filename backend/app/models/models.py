from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Numeric,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class RoleEnum(str, Enum):
    ADMIN = "admin"
    MOZO = "mozo"
    COCINA = "cocina"
    CAJA = "caja"


usuario_caja_association = Table(
    "usuario_caja_association",
    Base.metadata,
    mapped_column("usuario_id", ForeignKey("usuarios.id"), primary_key=True),
    mapped_column("caja_id", ForeignKey("cajas.id"), primary_key=True),
)


class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username_lower: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(128))
    rol: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255))
    pin_hash: Mapped[str] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    cajas_asignadas: Mapped[List["Caja"]] = relationship(
        secondary=usuario_caja_association, back_populates="usuarios"
    )
    turnos: Mapped[List["Turno"]] = relationship(back_populates="usuario")


class Caja(Base, TimestampMixin):
    __tablename__ = "cajas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    usuarios: Mapped[List[Usuario]] = relationship(
        secondary=usuario_caja_association, back_populates="cajas_asignadas"
    )
    turnos: Mapped[List["Turno"]] = relationship(back_populates="caja")
    ventas: Mapped[List["Venta"]] = relationship(back_populates="caja")


class Turno(Base, TimestampMixin):
    __tablename__ = "turnos"

    id: Mapped[int] = mapped_column(primary_key=True)
    caja_id: Mapped[int] = mapped_column(ForeignKey("cajas.id"))
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    abierto_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cerrado_at: Mapped[Optional[datetime]]
    arqueo_ciego: Mapped[bool] = mapped_column(Boolean, default=False)
    saldo_inicial: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    saldo_final: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    observaciones: Mapped[Optional[str]] = mapped_column(Text)

    caja: Mapped[Caja] = relationship(back_populates="turnos")
    usuario: Mapped[Usuario] = relationship(back_populates="turnos")
    movimientos: Mapped[List["MovimientoCaja"]] = relationship(back_populates="turno")
    ventas: Mapped[List["Venta"]] = relationship(back_populates="turno")


class MovimientoTipo(str, Enum):
    INGRESO = "ingreso"
    EGRESO = "egreso"


class MovimientoOrigen(str, Enum):
    VENTA = "venta"
    GASTO = "gasto"
    MANUAL = "manual"


class MovimientoCaja(Base, TimestampMixin):
    __tablename__ = "movimientos_caja"

    id: Mapped[int] = mapped_column(primary_key=True)
    turno_id: Mapped[int] = mapped_column(ForeignKey("turnos.id"))
    tipo: Mapped[MovimientoTipo] = mapped_column(SqlEnum(MovimientoTipo))
    origen: Mapped[MovimientoOrigen] = mapped_column(SqlEnum(MovimientoOrigen))
    monto: Mapped[float] = mapped_column(Numeric(12, 2))
    medio_pago: Mapped[str] = mapped_column(String(50))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    turno: Mapped[Turno] = relationship(back_populates="movimientos")


class Cliente(Base, TimestampMixin):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(150))
    descuento_pct: Mapped[Optional[float]] = mapped_column(Float)
    cta_corriente_saldo: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    ventas: Mapped[List["Venta"]] = relationship(back_populates="cliente")


class Proveedor(Base, TimestampMixin):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    categoria_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categorias_productos.id"))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(150))
    cta_corriente_saldo: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    categoria: Mapped[Optional["CategoriaProducto"]] = relationship(back_populates="proveedores")
    gastos: Mapped[List["Gasto"]] = relationship(back_populates="proveedor")


class CategoriaProducto(Base, TimestampMixin):
    __tablename__ = "categorias_productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categorias_productos.id"))

    parent: Mapped[Optional["CategoriaProducto"]] = relationship(remote_side="CategoriaProducto.id")
    productos: Mapped[List["Producto"]] = relationship(back_populates="categoria")
    ingredientes: Mapped[List["Ingrediente"]] = relationship(back_populates="categoria")
    proveedores: Mapped[List[Proveedor]] = relationship(back_populates="categoria")


class Producto(Base, TimestampMixin):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    sku: Mapped[str] = mapped_column(String(64), unique=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias_productos.id"))
    precio_lista: Mapped[float] = mapped_column(Numeric(12, 2))
    controla_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    favoritos: Mapped[bool] = mapped_column(Boolean, default=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    categoria: Mapped[CategoriaProducto] = relationship(back_populates="productos")
    lista_precios: Mapped[List["ListaPrecioItem"]] = relationship(back_populates="producto")
    receta: Mapped[Optional["Receta"]] = relationship(back_populates="producto")
    venta_items: Mapped[List["VentaItem"]] = relationship(back_populates="producto")


class Ingrediente(Base, TimestampMixin):
    __tablename__ = "ingredientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    categoria_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categorias_productos.id"))
    stock_actual: Mapped[float] = mapped_column(Float, default=0)
    stock_minimo: Mapped[float] = mapped_column(Float, default=0)
    unidad: Mapped[str] = mapped_column(String(20))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    categoria: Mapped[Optional[CategoriaProducto]] = relationship(back_populates="ingredientes")
    subingredientes: Mapped[List["SubIngrediente"]] = relationship(back_populates="padre")
    receta_items: Mapped[List["RecetaItem"]] = relationship(back_populates="ingrediente")


class SubIngrediente(Base, TimestampMixin):
    __tablename__ = "subingredientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    padre_id: Mapped[int] = mapped_column(ForeignKey("ingredientes.id"))
    nombre: Mapped[str] = mapped_column(String(150))
    factor: Mapped[float] = mapped_column(Float, default=1.0)

    padre: Mapped[Ingrediente] = relationship(back_populates="subingredientes")


class Receta(Base, TimestampMixin):
    __tablename__ = "recetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), unique=True)

    producto: Mapped[Producto] = relationship(back_populates="receta", foreign_keys=[producto_id])
    items: Mapped[List["RecetaItem"]] = relationship(back_populates="receta", cascade="all, delete-orphan")


class RecetaItem(Base):
    __tablename__ = "receta_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    receta_id: Mapped[int] = mapped_column(ForeignKey("recetas.id"))
    ingrediente_id: Mapped[int] = mapped_column(ForeignKey("ingredientes.id"))
    cantidad: Mapped[float] = mapped_column(Float, default=0)

    receta: Mapped[Receta] = relationship(back_populates="items")
    ingrediente: Mapped[Ingrediente] = relationship(back_populates="receta_items")


class ListaPrecio(Base, TimestampMixin):
    __tablename__ = "listas_precio"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True)
    activa: Mapped[bool] = mapped_column(Boolean, default=False)

    items: Mapped[List["ListaPrecioItem"]] = relationship(back_populates="lista", cascade="all, delete-orphan")


class ListaPrecioItem(Base, TimestampMixin):
    __tablename__ = "listas_precio_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    lista_id: Mapped[int] = mapped_column(ForeignKey("listas_precio.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    precio: Mapped[float] = mapped_column(Numeric(12, 2))

    lista: Mapped[ListaPrecio] = relationship(back_populates="items")
    producto: Mapped[Producto] = relationship(back_populates="lista_precios")


class VentaTipo(str, Enum):
    MESA = "mesa"
    MOSTRADOR = "mostrador"
    ONLINE = "online"


class VentaEstado(str, Enum):
    ABIERTA = "abierta"
    CERRADA = "cerrada"
    ANULADA = "anulada"


class Venta(Base, TimestampMixin):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[VentaTipo] = mapped_column(SqlEnum(VentaTipo))
    mesa_id: Mapped[Optional[int]] = mapped_column(ForeignKey("mesas.id"))
    cliente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("clientes.id"))
    mozo_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    caja_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cajas.id"))
    turno_id: Mapped[Optional[int]] = mapped_column(ForeignKey("turnos.id"))
    estado: Mapped[VentaEstado] = mapped_column(SqlEnum(VentaEstado), default=VentaEstado.ABIERTA)
    total_bruto: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    total_descuento: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    total_neto: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    propina: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    cliente: Mapped[Optional[Cliente]] = relationship(back_populates="ventas")
    mozo: Mapped[Usuario] = relationship()
    caja: Mapped[Optional[Caja]] = relationship(back_populates="ventas")
    turno: Mapped[Optional[Turno]] = relationship(back_populates="ventas")
    mesa: Mapped[Optional["Mesa"]] = relationship(back_populates="ventas")
    items: Mapped[List["VentaItem"]] = relationship(back_populates="venta", cascade="all, delete-orphan")
    pagos: Mapped[List["Pago"]] = relationship(back_populates="venta", cascade="all, delete-orphan")
    descuentos: Mapped[List["Descuento"]] = relationship(back_populates="venta")
    pedidos_cocina: Mapped[List["PedidoCocina"]] = relationship(back_populates="venta")


class VentaItem(Base, TimestampMixin):
    __tablename__ = "ventas_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    cantidad: Mapped[float] = mapped_column(Float, default=1)
    precio_unitario: Mapped[float] = mapped_column(Numeric(12, 2))
    modificadores: Mapped[Optional[List[dict]]] = mapped_column(JSON)

    venta: Mapped[Venta] = relationship(back_populates="items")
    producto: Mapped[Producto] = relationship(back_populates="venta_items")


class MedioPago(str, Enum):
    EFECTIVO = "efectivo"
    MP_QR = "mp_qr"
    MP_LINK = "mp_link"
    DEBITO = "debito"
    CREDITO = "credito"
    TRANSFER = "transfer"
    OTROS = "otros"


class Pago(Base, TimestampMixin):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    medio: Mapped[MedioPago] = mapped_column(SqlEnum(MedioPago))
    monto: Mapped[float] = mapped_column(Numeric(12, 2))
    referencia: Mapped[Optional[str]] = mapped_column(String(255))

    venta: Mapped[Venta] = relationship(back_populates="pagos")


class DescuentoTipo(str, Enum):
    FIJO = "fijo"
    PORCENTUAL = "porcentual"


class Descuento(Base, TimestampMixin):
    __tablename__ = "descuentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[DescuentoTipo] = mapped_column(SqlEnum(DescuentoTipo))
    valor: Mapped[float] = mapped_column(Float)
    motivo: Mapped[Optional[str]] = mapped_column(String(255))
    venta_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ventas.id"))
    cliente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("clientes.id"))

    venta: Mapped[Optional[Venta]] = relationship(back_populates="descuentos")
    cliente: Mapped[Optional[Cliente]] = relationship()


class Mesa(Base, TimestampMixin):
    __tablename__ = "mesas"

    id: Mapped[int] = mapped_column(primary_key=True)
    sala: Mapped[str] = mapped_column(String(150))
    numero: Mapped[str] = mapped_column(String(10))
    camarero_id: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id"))

    ventas: Mapped[List[Venta]] = relationship(back_populates="mesa")

    __table_args__ = (CheckConstraint("numero != ''", name="ck_mesas_numero_not_empty"),)


class Gasto(Base, TimestampMixin):
    __tablename__ = "gastos"

    id: Mapped[int] = mapped_column(primary_key=True)
    proveedor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("proveedores.id"))
    categoria_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categorias_productos.id"))
    monto: Mapped[float] = mapped_column(Numeric(12, 2))
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    vence_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    items: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    actualiza_costos: Mapped[bool] = mapped_column(Boolean, default=False)
    actualiza_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    medio_pago: Mapped[Optional[str]] = mapped_column(String(50))

    proveedor: Mapped[Optional[Proveedor]] = relationship(back_populates="gastos")
    categoria: Mapped[Optional[CategoriaProducto]] = relationship()


class StockMovimientoTipo(str, Enum):
    COMPRA = "compra"
    VENTA = "venta"
    AJUSTE = "ajuste"
    MERMA = "merma"
    DESPERDICIO = "desperdicio"
    RECETA = "receta"


class StockMovimiento(Base, TimestampMixin):
    __tablename__ = "stock_movimientos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[StockMovimientoTipo] = mapped_column(SqlEnum(StockMovimientoTipo))
    ref_id: Mapped[Optional[int]]
    ingrediente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ingredientes.id"))
    producto_id: Mapped[Optional[int]] = mapped_column(ForeignKey("productos.id"))
    delta: Mapped[float] = mapped_column(Float)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    motivo: Mapped[Optional[str]] = mapped_column(String(255))

    ingrediente: Mapped[Optional[Ingrediente]] = relationship()
    producto: Mapped[Optional[Producto]] = relationship()


class PedidoCocinaEstado(str, Enum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    LISTO = "listo"


class PedidoCocina(Base, TimestampMixin):
    __tablename__ = "pedidos_cocina"

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    estado: Mapped[PedidoCocinaEstado] = mapped_column(
        SqlEnum(PedidoCocinaEstado), default=PedidoCocinaEstado.PENDIENTE
    )
    items: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    timestamps: Mapped[Optional[dict]] = mapped_column(JSON)

    venta: Mapped[Venta] = relationship(back_populates="pedidos_cocina")


class Config(Base, TimestampMixin):
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(primary_key=True)
    k: Mapped[str] = mapped_column(String(150), unique=True)
    v: Mapped[str] = mapped_column(Text)


class ReporteCache(Base, TimestampMixin):
    __tablename__ = "reportes_cache"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(100))
    rango_desde: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    rango_hasta: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    payload_json: Mapped[Optional[dict]] = mapped_column(JSON)
    generado_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
