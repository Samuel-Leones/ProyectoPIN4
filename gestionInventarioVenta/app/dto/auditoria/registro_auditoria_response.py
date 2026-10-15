from app.dto.base import DtoAuditoria
from app.model.accion_auditoria import AccionAuditoria


class RegistroAuditoriaResponse(DtoAuditoria):
    id: int
    usuario_id: int
    correo_usuario: str
    accion: AccionAuditoria
    entidad_afectada: str
    id_entidad_afectada: int
