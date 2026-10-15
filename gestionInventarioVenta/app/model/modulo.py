from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.base_datos import Base, CamposComunes, TipoId


class Modulo(CamposComunes, Base):
    __tablename__ = "modulos"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ruta: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    icono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
