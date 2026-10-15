from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.producto import Producto


class ProductoCompatibilidad(CamposComunes, Base):
    __tablename__ = "productos_compatibilidad"
    __table_args__ = (
        UniqueConstraint("producto_id", "version_moto_id", name="uq_producto_version_moto"),
        Index("ix_productos_compatibilidad_version_moto", "version_moto_id"),
    )

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    producto_id: Mapped[int] = mapped_column(TipoId, ForeignKey("productos.id"), nullable=False)
    version_moto_id: Mapped[int] = mapped_column(TipoId, nullable=False)
    descripcion_moto: Mapped[str] = mapped_column(String(255), nullable=False)

    producto: Mapped[Producto] = relationship(lazy="select")
