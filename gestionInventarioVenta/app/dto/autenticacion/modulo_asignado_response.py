from typing import Optional

from app.dto.base import DtoBase


class ModuloAsignadoResponse(DtoBase):

    modulo_id: int
    nombre: str
    descripcion: Optional[str]
    ruta: str
    icono: Optional[str]
    puede_crear: bool
    puede_editar: bool
    puede_eliminar: bool
