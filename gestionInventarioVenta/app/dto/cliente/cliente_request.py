from typing import Optional

from app.dto.base import DtoBase
from app.dto.validaciones import EmailOpcional, NotBlank


class ClienteRequest(DtoBase):
    nombre: NotBlank
    documento: NotBlank
    telefono: Optional[str] = None
    correo: EmailOpcional = None
    direccion: Optional[str] = None
