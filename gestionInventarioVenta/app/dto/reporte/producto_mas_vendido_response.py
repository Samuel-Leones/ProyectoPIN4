from app.dto.base import DtoBase


class ProductoMasVendidoResponse(DtoBase):
    producto_id: int
    nombre_producto: str
    cantidad_total_vendida: int
