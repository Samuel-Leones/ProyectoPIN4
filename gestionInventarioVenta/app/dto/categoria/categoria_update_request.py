from typing import Optional

from app.dto.base import DtoBase


class CategoriaUpdateRequest(DtoBase):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
