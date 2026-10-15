from app.dto.base import DtoBase


class TokenResponse(DtoBase):
    token_acceso: str
    tipo_token: str = "Bearer"
    expira_en_segundos: int
