from typing import Optional

from app.dto.base import DtoAuditoria


class RolResponse(DtoAuditoria):
    id: int
    nombre: str
    descripcion: Optional[str]
