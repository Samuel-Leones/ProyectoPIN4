from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.base_datos import Base, CamposComunes, TipoId


class Rol(CamposComunes, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
