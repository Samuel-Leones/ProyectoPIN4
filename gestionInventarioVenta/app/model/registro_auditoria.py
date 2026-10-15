from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.accion_auditoria import AccionAuditoria


class RegistroAuditoria(CamposComunes, Base):
    __tablename__ = "registros_auditoria"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(TipoId, nullable=False)
    correo_usuario: Mapped[str] = mapped_column(String(255), nullable=False)
    accion: Mapped[AccionAuditoria] = mapped_column(
        Enum(AccionAuditoria, native_enum=False, length=20), nullable=False
    )
    entidad_afectada: Mapped[str] = mapped_column(String(255), nullable=False)
    id_entidad_afectada: Mapped[int] = mapped_column(TipoId, nullable=False)
