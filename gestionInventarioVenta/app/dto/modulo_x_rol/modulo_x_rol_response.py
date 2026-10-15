from app.dto.base import DtoAuditoria


class ModuloXRolResponse(DtoAuditoria):
    id: int
    rol_id: int
    nombre_rol: str
    modulo_id: int
    nombre_modulo: str
    ruta_modulo: str
    puede_crear: bool
    puede_editar: bool
    puede_eliminar: bool
