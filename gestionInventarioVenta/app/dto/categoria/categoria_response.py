from typing import Optional

from app.dto.base import DtoAuditoria


class CategoriaResponse(DtoAuditoria):
    id: int
    nombre: str
    descripcion: Optional[str]
