from app.dto.base import DtoAuditoria
from app.dto.tipos import Dinero
from app.dto.venta.detalle_venta_response import DetalleVentaResponse
from app.model.estado_venta import EstadoVenta


class VentaResponse(DtoAuditoria):
    id: int
    cliente_id: int
    nombre_cliente: str
    vendedor_id: int
    correo_vendedor: str
    subtotal: Dinero
    iva: Dinero
    total: Dinero
    estado_venta: EstadoVenta
    detalles: list[DetalleVentaResponse]
