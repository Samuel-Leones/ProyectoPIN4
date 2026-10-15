from app.dto.base import DtoBase
from app.dto.tipos import Dinero


class EstadisticasPanelResponse(DtoBase):
    total_ventas_del_mes: Dinero
    cantidad_productos_activos: int
    cantidad_productos_agotados: int
    cantidad_clientes_registrados: int
