from typing import Optional

from sqlalchemy import Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.config.base_datos import Base, CamposComunes, TipoId


class Cliente(CamposComunes, Base):
    __tablename__ = "clientes"
    __table_args__ = (
        Index("uq_clientes_documento_activo", "documento", unique=True, postgresql_where=text("estado")),
    )

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    documento: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    correo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    direccion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
