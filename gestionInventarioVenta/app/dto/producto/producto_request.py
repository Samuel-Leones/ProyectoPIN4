from decimal import Decimal
from typing import Optional

from app.dto.base import DtoBase
from app.dto.validaciones import NotBlank, PositivoOCero, PrecioPositivo


class ProductoRequest(DtoBase):
    nombre: NotBlank
    descripcion: Optional[str] = None
    codigo: NotBlank
    categoria_id: int
    proveedor_id: Optional[int] = None
    precio: PrecioPositivo
    stock_inicial: PositivoOCero = 0
    stock_minimo: PositivoOCero = 0
