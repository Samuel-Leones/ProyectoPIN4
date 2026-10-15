from sqlalchemy import Boolean, ForeignKey, UniqueConstraint, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.modulo import Modulo
from app.model.rol import Rol


class ModuloXRol(CamposComunes, Base):
    __tablename__ = "modulo_x_rol"
    __table_args__ = (UniqueConstraint("rol_id", "modulo_id", name="uq_modulo_x_rol"),)

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    rol_id: Mapped[int] = mapped_column(TipoId, ForeignKey("roles.id"), nullable=False)
    modulo_id: Mapped[int] = mapped_column(TipoId, ForeignKey("modulos.id"), nullable=False)
    puede_crear: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    puede_editar: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    puede_eliminar: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())

    rol: Mapped[Rol] = relationship(lazy="select")
    modulo: Mapped[Modulo] = relationship(lazy="select")
