from app.dto.base import DtoBase
from app.dto.tipos import Dinero


class DetalleVentaResponse(DtoBase):
    producto_id: int
    nombre_producto: str
    cantidad: int
    precio_unitario: Dinero
    total_linea: Dinero
