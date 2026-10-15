from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.rol import Rol


class Usuario(CamposComunes, Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    correo: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nombre_completo: Mapped[str] = mapped_column(String(255), nullable=False)
    contrasena: Mapped[str] = mapped_column(String(255), nullable=False)
    rol_id: Mapped[int] = mapped_column(TipoId, ForeignKey("roles.id"), nullable=False)

    rol: Mapped[Rol] = relationship(lazy="select")
