from app.dto.base import DtoBase
from app.dto.validaciones import ContrasenaValida, NotBlank, NotBlankEmail


class RegistroRequest(DtoBase):
    correo: NotBlankEmail
    nombre_completo: NotBlank
    contrasena: ContrasenaValida
    rol_id: int
