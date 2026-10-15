from typing import Optional

from app.dto.base import DtoBase
from app.dto.validaciones import NotBlank


class ModuloRequest(DtoBase):
    nombre: NotBlank
    descripcion: Optional[str] = None
    ruta: NotBlank
    icono: Optional[str] = None
