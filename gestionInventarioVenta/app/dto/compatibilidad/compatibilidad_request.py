from app.dto.base import DtoBase
from app.dto.validaciones import Positivo


class CompatibilidadRequest(DtoBase):
    version_moto_id: Positivo
