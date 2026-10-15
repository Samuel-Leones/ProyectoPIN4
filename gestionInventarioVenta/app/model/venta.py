from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.cliente import Cliente
from app.model.estado_venta import EstadoVenta
from app.model.usuario import Usuario

if TYPE_CHECKING:
    from app.model.detalle_venta import DetalleVenta


class Venta(CamposComunes, Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(TipoId, ForeignKey("clientes.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(TipoId, ForeignKey("usuarios.id"), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    iva: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    estado_venta: Mapped[EstadoVenta] = mapped_column(
        Enum(EstadoVenta, native_enum=False, length=20),
        nullable=False,
        default=EstadoVenta.PENDIENTE,
    )

    cliente: Mapped[Cliente] = relationship(lazy="select")
    vendedor: Mapped[Usuario] = relationship(lazy="select", foreign_keys=[usuario_id])
    detalles: Mapped[list["DetalleVenta"]] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan",
        order_by="DetalleVenta.id",
        lazy="select",
    )
