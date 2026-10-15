from sqlalchemy import select

from app.model.registro_auditoria import RegistroAuditoria
from app.repository.repositorio_jpa import RepositorioJpa


class RegistroAuditoriaRepository(RepositorioJpa[RegistroAuditoria]):
    modelo = RegistroAuditoria

    def find_all_by_order_by_creado_desc(self) -> list[RegistroAuditoria]:
        consulta = select(RegistroAuditoria).order_by(RegistroAuditoria.creado.desc(), RegistroAuditoria.id.desc())
        return list(self.db.scalars(consulta).all())

    def find_all_by_entidad_afectada_order_by_creado_desc(self, entidad_afectada: str) -> list[RegistroAuditoria]:
        consulta = (
            select(RegistroAuditoria)
            .where(RegistroAuditoria.entidad_afectada == entidad_afectada)
            .order_by(RegistroAuditoria.creado.desc(), RegistroAuditoria.id.desc())
        )
        return list(self.db.scalars(consulta).all())
