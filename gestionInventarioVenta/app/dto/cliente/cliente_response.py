from typing import Optional

from app.dto.base import DtoAuditoria


class ClienteResponse(DtoAuditoria):
    id: int
    nombre: str
    documento: str
    telefono: Optional[str]
    correo: Optional[str]
    direccion: Optional[str]
