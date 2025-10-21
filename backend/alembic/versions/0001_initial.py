"""initial schema"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def timestamp_columns() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    ]


def upgrade() -> None:
    role_enum = sa.Enum("admin", "mozo", "cocina", "caja", name="roleenum")
    movimiento_tipo = sa.Enum("ingreso", "egreso", name="movimientotipo")
    movimiento_origen = sa.Enum("venta", "gasto", "manual", name="movimientoorigen")
    venta_tipo = sa.Enum("mesa", "mostrador", "online", name="ventatipo")
    venta_estado = sa.Enum("abierta", "cerrada", "anulada", name="ventaestado")
    medio_pago = sa.Enum(
        "efectivo",
        "mp_qr",
        "mp_link",
        "debito",
        "credito",
        "transfer",
        "otros",
        name="mediopago",
    )
    descuento_tipo = sa.Enum("fijo", "porcentual", name="descuentotipo")
    stock_tipo = sa.Enum(
        "compra",
        "venta",
        "ajuste",
        "merma",
        "desperdicio",
        "receta",
        name="stockmovimientotipo",
    )
    pedido_estado = sa.Enum("pendiente", "en_curso", "listo", name="pedidococinaestado")

    bind = op.get_bind()
    for enum in [
        role_enum,
        movimiento_tipo,
        movimiento_origen,
        venta_tipo,
        venta_estado,
        medio_pago,
        descuento_tipo,
        stock_tipo,
        pedido_estado,
    ]:
        enum.create(bind, checkfirst=True)

    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username_lower", sa.String(length=64), nullable=False, unique=True),
        sa.Column("nombre", sa.String(length=128), nullable=False),
        sa.Column("rol", role_enum, nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("pin_hash", sa.String(length=255), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamp_columns(),
    )
    op.create_index("ix_usuarios_username_lower", "usuarios", ["username_lower"], unique=True)

    op.create_table(
        "cajas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=100), nullable=False, unique=True),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamp_columns(),
    )

    op.create_table(
        "categorias_productos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=150), nullable=False, unique=True),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("categorias_productos.id"), nullable=True),
        *timestamp_columns(),
    )

    op.create_table(
        "clientes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("telefono", sa.String(length=50)),
        sa.Column("email", sa.String(length=150)),
        sa.Column("descuento_pct", sa.Float()),
        sa.Column("cta_corriente_saldo", sa.Numeric(12, 2), nullable=False, server_default="0"),
        *timestamp_columns(),
    )

    op.create_table(
        "config",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("k", sa.String(length=150), nullable=False, unique=True),
        sa.Column("v", sa.Text(), nullable=False),
        *timestamp_columns(),
    )

    op.create_table(
        "proveedores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("categoria_id", sa.Integer(), sa.ForeignKey("categorias_productos.id")),
        sa.Column("telefono", sa.String(length=50)),
        sa.Column("email", sa.String(length=150)),
        sa.Column("cta_corriente_saldo", sa.Numeric(12, 2), nullable=False, server_default="0"),
        *timestamp_columns(),
    )

    op.create_table(
        "ingredientes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("categoria_id", sa.Integer(), sa.ForeignKey("categorias_productos.id")),
        sa.Column("stock_actual", sa.Float(), nullable=False, server_default="0"),
        sa.Column("stock_minimo", sa.Float(), nullable=False, server_default="0"),
        sa.Column("unidad", sa.String(length=20), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamp_columns(),
    )

    op.create_table(
        "listas_precio",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=150), nullable=False, unique=True),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        *timestamp_columns(),
    )

    op.create_table(
        "mesas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sala", sa.String(length=150), nullable=False),
        sa.Column("numero", sa.String(length=10), nullable=False),
        sa.Column("camarero_id", sa.Integer(), sa.ForeignKey("usuarios.id")),
        sa.CheckConstraint("numero != ''", name="ck_mesas_numero_not_empty"),
        *timestamp_columns(),
    )

    op.create_table(
        "productos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=200), nullable=False),
        sa.Column("sku", sa.String(length=64), nullable=False, unique=True),
        sa.Column("categoria_id", sa.Integer(), sa.ForeignKey("categorias_productos.id"), nullable=False),
        sa.Column("precio_lista", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("controla_stock", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("favoritos", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamp_columns(),
    )

    op.create_table(
        "reportes_cache",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tipo", sa.String(length=100), nullable=False),
        sa.Column("rango_desde", sa.DateTime(timezone=True)),
        sa.Column("rango_hasta", sa.DateTime(timezone=True)),
        sa.Column("payload_json", sa.JSON(), nullable=True),
        sa.Column("generado_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        *timestamp_columns(),
    )

    op.create_table(
        "recetas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("producto_id", sa.Integer(), sa.ForeignKey("productos.id"), nullable=False, unique=True),
        *timestamp_columns(),
    )

    op.create_table(
        "subingredientes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("padre_id", sa.Integer(), sa.ForeignKey("ingredientes.id"), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("factor", sa.Float(), nullable=False, server_default="1"),
        *timestamp_columns(),
    )

    op.create_table(
        "usuario_caja_association",
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("caja_id", sa.Integer(), sa.ForeignKey("cajas.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "turnos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("caja_id", sa.Integer(), sa.ForeignKey("cajas.id"), nullable=False),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("abierto_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cerrado_at", sa.DateTime(timezone=True)),
        sa.Column("arqueo_ciego", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("saldo_inicial", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("saldo_final", sa.Numeric(12, 2)),
        sa.Column("observaciones", sa.Text()),
        *timestamp_columns(),
    )

    op.create_table(
        "gastos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("proveedor_id", sa.Integer(), sa.ForeignKey("proveedores.id")),
        sa.Column("categoria_id", sa.Integer(), sa.ForeignKey("categorias_productos.id")),
        sa.Column("monto", sa.Numeric(12, 2), nullable=False),
        sa.Column("fecha", sa.DateTime(timezone=True), nullable=False),
        sa.Column("vence_at", sa.DateTime(timezone=True)),
        sa.Column("items", sa.JSON()),
        sa.Column("actualiza_costos", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("actualiza_stock", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("medio_pago", sa.String(length=50)),
        *timestamp_columns(),
    )

    op.create_table(
        "listas_precio_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("lista_id", sa.Integer(), sa.ForeignKey("listas_precio.id"), nullable=False),
        sa.Column("producto_id", sa.Integer(), sa.ForeignKey("productos.id"), nullable=False),
        sa.Column("precio", sa.Numeric(12, 2), nullable=False),
        *timestamp_columns(),
    )

    op.create_table(
        "movimientos_caja",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("turno_id", sa.Integer(), sa.ForeignKey("turnos.id"), nullable=False),
        sa.Column("tipo", movimiento_tipo, nullable=False),
        sa.Column("origen", movimiento_origen, nullable=False),
        sa.Column("monto", sa.Numeric(12, 2), nullable=False),
        sa.Column("medio_pago", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.Text()),
        *timestamp_columns(),
    )

    op.create_table(
        "receta_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("receta_id", sa.Integer(), sa.ForeignKey("recetas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ingrediente_id", sa.Integer(), sa.ForeignKey("ingredientes.id"), nullable=False),
        sa.Column("cantidad", sa.Float(), nullable=False, server_default="0"),
    )

    op.create_table(
        "stock_movimientos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tipo", stock_tipo, nullable=False),
        sa.Column("ref_id", sa.Integer()),
        sa.Column("ingrediente_id", sa.Integer(), sa.ForeignKey("ingredientes.id")),
        sa.Column("producto_id", sa.Integer(), sa.ForeignKey("productos.id")),
        sa.Column("delta", sa.Float(), nullable=False),
        sa.Column("fecha", sa.DateTime(timezone=True), nullable=False),
        sa.Column("motivo", sa.String(length=255)),
        *timestamp_columns(),
    )

    op.create_table(
        "ventas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tipo", venta_tipo, nullable=False),
        sa.Column("mesa_id", sa.Integer(), sa.ForeignKey("mesas.id")),
        sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("clientes.id")),
        sa.Column("mozo_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("caja_id", sa.Integer(), sa.ForeignKey("cajas.id")),
        sa.Column("turno_id", sa.Integer(), sa.ForeignKey("turnos.id")),
        sa.Column("estado", venta_estado, nullable=False, server_default="abierta"),
        sa.Column("total_bruto", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total_descuento", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total_neto", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("propina", sa.Numeric(12, 2), nullable=False, server_default="0"),
        *timestamp_columns(),
    )

    op.create_table(
        "descuentos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tipo", descuento_tipo, nullable=False),
        sa.Column("valor", sa.Float(), nullable=False),
        sa.Column("motivo", sa.String(length=255)),
        sa.Column("venta_id", sa.Integer(), sa.ForeignKey("ventas.id")),
        sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("clientes.id")),
        *timestamp_columns(),
    )

    op.create_table(
        "pedidos_cocina",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("venta_id", sa.Integer(), sa.ForeignKey("ventas.id"), nullable=False),
        sa.Column("estado", pedido_estado, nullable=False, server_default="pendiente"),
        sa.Column("items", sa.JSON()),
        sa.Column("timestamps", sa.JSON()),
        *timestamp_columns(),
    )

    op.create_table(
        "pagos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("venta_id", sa.Integer(), sa.ForeignKey("ventas.id"), nullable=False),
        sa.Column("medio", medio_pago, nullable=False),
        sa.Column("monto", sa.Numeric(12, 2), nullable=False),
        sa.Column("referencia", sa.String(length=255)),
        *timestamp_columns(),
    )

    op.create_table(
        "ventas_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("venta_id", sa.Integer(), sa.ForeignKey("ventas.id"), nullable=False),
        sa.Column("producto_id", sa.Integer(), sa.ForeignKey("productos.id"), nullable=False),
        sa.Column("cantidad", sa.Float(), nullable=False, server_default="1"),
        sa.Column("precio_unitario", sa.Numeric(12, 2), nullable=False),
        sa.Column("modificadores", sa.JSON()),
        *timestamp_columns(),
    )


def downgrade() -> None:
    raise NotImplementedError("Downgrade no soportado en esta versión inicial")
