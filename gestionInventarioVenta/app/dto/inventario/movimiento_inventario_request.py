from typing import Optional

from app.dto.base import DtoBase
from app.dto.validaciones import Positivo
from app.model.tipo_movimiento_inventario import TipoMovimientoInventario


class MovimientoInventarioRequest(DtoBase):
    producto_id: int
    tipo: TipoMovimientoInventario
    cantidad: Positivo
    motivo: Optional[str] = None
