from typing import Optional

from app.dto.base import DtoBase


class ClienteUpdateRequest(DtoBase):
    nombre: Optional[str] = None
    documento: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None
