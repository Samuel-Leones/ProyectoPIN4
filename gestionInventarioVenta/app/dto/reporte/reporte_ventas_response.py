from app.dto.base import DtoBase
from app.dto.tipos import Dinero


class ReporteVentasResponse(DtoBase):
    etiqueta_periodo: str
    total_ventas: Dinero
    cantidad_transacciones: int
