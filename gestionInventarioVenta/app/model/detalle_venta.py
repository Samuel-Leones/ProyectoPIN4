from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.producto import Producto
from app.model.venta import Venta


class DetalleVenta(CamposComunes, Base):
    __tablename__ = "detalles_venta"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    venta_id: Mapped[int] = mapped_column(TipoId, ForeignKey("ventas.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(TipoId, ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)

    venta: Mapped[Venta] = relationship(back_populates="detalles", lazy="select")
    producto: Mapped[Producto] = relationship(lazy="select")
