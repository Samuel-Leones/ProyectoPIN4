from app.dto.base import DtoBase


class ModuloXRolRequest(DtoBase):
    rol_id: int
    modulo_id: int
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False
