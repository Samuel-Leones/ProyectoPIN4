from app.dto.base import DtoBase
from app.dto.validaciones import Positivo


class ItemVentaRequest(DtoBase):
    producto_id: int
    cantidad: Positivo
