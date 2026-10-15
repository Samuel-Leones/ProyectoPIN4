from app.dto.base import DtoAuditoria
from app.dto.venta.venta_response import VentaResponse


class FacturaResponse(DtoAuditoria):
    id: int
    numero_factura: str
    venta: VentaResponse
