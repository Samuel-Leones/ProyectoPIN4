from typing import Optional

from app.dto.base import DtoBase
from app.dto.validaciones import NotBlank


class CategoriaRequest(DtoBase):
    nombre: NotBlank
    descripcion: Optional[str] = None
