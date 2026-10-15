from typing import Optional

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.producto import Producto
from app.model.tipo_movimiento_inventario import TipoMovimientoInventario
from app.model.usuario import Usuario


class MovimientoInventario(CamposComunes, Base):
    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    producto_id: Mapped[int] = mapped_column(TipoId, ForeignKey("productos.id"), nullable=False)
    tipo: Mapped[TipoMovimientoInventario] = mapped_column(
        Enum(TipoMovimientoInventario, native_enum=False, length=20), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    usuario_id: Mapped[int] = mapped_column(TipoId, ForeignKey("usuarios.id"), nullable=False)

    producto: Mapped[Producto] = relationship(lazy="select")
    usuario: Mapped[Usuario] = relationship(lazy="select")
