from typing import Optional

from sqlalchemy import Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.config.base_datos import Base, CamposComunes, TipoId


class Proveedor(CamposComunes, Base):
    __tablename__ = "proveedores"
    __table_args__ = (
        Index("uq_proveedores_nombre_activo", "nombre", unique=True, postgresql_where=text("estado")),
    )

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre_contacto: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    correo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
