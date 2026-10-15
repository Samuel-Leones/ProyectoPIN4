from app.dto.base import DtoBase


class ModuloXRolUpdateRequest(DtoBase):
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False
