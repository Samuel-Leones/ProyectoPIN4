from app.dto.base import DtoBase


class ReporteInventarioItemResponse(DtoBase):
    producto_id: int
    nombre_producto: str
    codigo: str
    stock_actual: int
    stock_minimo: int
    stock_bajo: bool
