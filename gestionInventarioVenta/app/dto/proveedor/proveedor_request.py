from typing import Optional

from app.dto.base import DtoBase
from app.dto.validaciones import EmailOpcional, NotBlank


class ProveedorRequest(DtoBase):
    nombre: NotBlank
    nombre_contacto: Optional[str] = None
    telefono: Optional[str] = None
    correo: EmailOpcional = None
