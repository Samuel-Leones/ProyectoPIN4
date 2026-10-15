from typing import Optional

from app.dto.base import DtoAuditoria
from app.model.tipo_movimiento_inventario import TipoMovimientoInventario


class MovimientoInventarioResponse(DtoAuditoria):
    id: int
    producto_id: int
    nombre_producto: str
    tipo: TipoMovimientoInventario
    cantidad: int
    motivo: Optional[str]
    stock_resultante: int
    correo_usuario: str
