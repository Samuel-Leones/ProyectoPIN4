from app.dto.panel.estadisticas_panel_response import EstadisticasPanelResponse
from app.model.estado_venta import EstadoVenta
from app.repository.cliente_repository import ClienteRepository
from app.repository.producto_repository import ProductoRepository
from app.repository.venta_repository import VentaRepository
from app.util.anio_mes import AnioMes, inicio_del_dia


class ServicioPanel:
    def __init__(
        self,
        venta_repository: VentaRepository,
        producto_repository: ProductoRepository,
        cliente_repository: ClienteRepository,
    ):
        self.venta_repository = venta_repository
        self.producto_repository = producto_repository
        self.cliente_repository = cliente_repository

    def obtener_estadisticas(self) -> EstadisticasPanelResponse:
        mes_actual = AnioMes.now()
        desde = inicio_del_dia(mes_actual.at_day(1))
        hasta = inicio_del_dia(mes_actual.plus_months(1).at_day(1))

        return EstadisticasPanelResponse(
            total_ventas_del_mes=self.venta_repository.sumar_total_por_estado_y_fecha(
                EstadoVenta.COMPLETADA, desde, hasta
            ),
            cantidad_productos_activos=self.producto_repository.count_by_estado_true(),
            cantidad_productos_agotados=self.producto_repository.count_by_estado_true_and_stock_actual(0),
            cantidad_clientes_registrados=self.cliente_repository.count_by_estado_true(),
        )
