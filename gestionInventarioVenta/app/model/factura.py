from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.venta import Venta


class Factura(CamposComunes, Base):
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    venta_id: Mapped[int] = mapped_column(TipoId, ForeignKey("ventas.id"), nullable=False, unique=True)
    numero_factura: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    venta: Mapped[Venta] = relationship(lazy="select")
