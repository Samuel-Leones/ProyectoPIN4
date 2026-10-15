from typing import Optional

from app.dto.auditoria.registro_auditoria_response import RegistroAuditoriaResponse
from app.dto.base import campos_auditoria
from app.model.accion_auditoria import AccionAuditoria
from app.model.registro_auditoria import RegistroAuditoria
from app.repository.registro_auditoria_repository import RegistroAuditoriaRepository
from app.repository.usuario_repository import UsuarioRepository


class ServicioAuditoria:
    def __init__(
        self,
        registro_auditoria_repository: RegistroAuditoriaRepository,
        usuario_repository: UsuarioRepository,
    ):
        self.registro_auditoria_repository = registro_auditoria_repository
        self.usuario_repository = usuario_repository

    def registrar(self, correo_responsable: str, accion: AccionAuditoria, entidad: str, id_entidad: int) -> None:
        usuario = self.usuario_repository.find_by_correo(correo_responsable)
        if usuario is None:
            return

        registro = RegistroAuditoria(
            usuario_id=usuario.id,
            correo_usuario=usuario.correo,
            accion=accion,
            entidad_afectada=entidad,
            id_entidad_afectada=id_entidad,
        )
        self.registro_auditoria_repository.save(registro)

    def obtener_registros(self, entidad: Optional[str]) -> list[RegistroAuditoriaResponse]:
        if entidad is None or entidad.strip() == "":
            registros = self.registro_auditoria_repository.find_all_by_order_by_creado_desc()
        else:
            registros = self.registro_auditoria_repository.find_all_by_entidad_afectada_order_by_creado_desc(entidad)
        return [self._a_response(r) for r in registros]

    @staticmethod
    def _a_response(registro: RegistroAuditoria) -> RegistroAuditoriaResponse:
        return RegistroAuditoriaResponse(
            id=registro.id,
            usuario_id=registro.usuario_id,
            correo_usuario=registro.correo_usuario,
            accion=registro.accion,
            entidad_afectada=registro.entidad_afectada,
            id_entidad_afectada=registro.id_entidad_afectada,
            **campos_auditoria(registro),
        )
