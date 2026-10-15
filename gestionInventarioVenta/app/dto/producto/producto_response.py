from typing import Optional

from app.dto.base import DtoAuditoria
from app.dto.tipos import Dinero


class ProductoResponse(DtoAuditoria):
    id: int
    nombre: str
    descripcion: Optional[str]
    codigo: str
    categoria_id: int
    nombre_categoria: str
    proveedor_id: Optional[int]
    nombre_proveedor: Optional[str]
    precio: Dinero
    stock_actual: int
    stock_minimo: int
    stock_bajo: bool
    mensaje_alerta: Optional[str]
