from typing import Optional

from app.dto.base import DtoAuditoria


class ProveedorResponse(DtoAuditoria):
    id: int
    nombre: str
    nombre_contacto: Optional[str]
    telefono: Optional[str]
    correo: Optional[str]
