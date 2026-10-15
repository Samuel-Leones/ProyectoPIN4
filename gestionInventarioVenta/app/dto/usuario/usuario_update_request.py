from typing import Optional

from app.dto.base import DtoBase
from app.dto.validaciones import ContrasenaOpcional


class UsuarioUpdateRequest(DtoBase):
    nombre_completo: Optional[str] = None
    rol_id: Optional[int] = None
    contrasena: ContrasenaOpcional = None
