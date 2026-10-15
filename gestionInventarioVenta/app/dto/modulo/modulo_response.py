from typing import Optional

from app.dto.base import DtoAuditoria


class ModuloResponse(DtoAuditoria):
    id: int
    nombre: str
    descripcion: Optional[str]
    ruta: str
    icono: Optional[str]
