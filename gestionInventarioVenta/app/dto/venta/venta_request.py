from typing import Annotated

from app.dto.base import DtoBase
from app.dto.validaciones import ListaVentaNoVacia
from app.dto.venta.item_venta_request import ItemVentaRequest


class VentaRequest(DtoBase):
    cliente_id: int
    items: Annotated[list[ItemVentaRequest], ListaVentaNoVacia]
