from app.dto.base import DtoAuditoria


class UsuarioResponse(DtoAuditoria):
    id: int
    correo: str
    nombre_completo: str
    rol_id: int
    rol: str
