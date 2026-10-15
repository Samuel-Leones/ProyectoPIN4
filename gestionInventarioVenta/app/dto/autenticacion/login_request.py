from app.dto.base import DtoBase
from app.dto.validaciones import NotBlank, NotBlankEmail


class LoginRequest(DtoBase):
    correo: NotBlankEmail
    contrasena: NotBlank
