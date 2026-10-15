from datetime import date, timedelta

from app.dto.reporte.producto_mas_vendido_response import ProductoMasVendidoResponse
from app.dto.reporte.reporte_inventario_item_response import ReporteInventarioItemResponse
from app.dto.reporte.reporte_ventas_response import ReporteVentasResponse
from app.model.estado_venta import EstadoVenta
from app.repository.detalle_venta_repository import DetalleVentaRepository
from app.repository.producto_repository import ProductoRepository
from app.repository.venta_repository import VentaRepository
from app.util.anio_mes import AnioMes, inicio_del_dia


class ServicioReporte:
    def __init__(
        self,
        venta_repository: VentaRepository,
        detalle_venta_repository: DetalleVentaRepository,
        producto_repository: ProductoRepository,
    ):
        self.venta_repository = venta_repository
        self.detalle_venta_repository = detalle_venta_repository
        self.producto_repository = producto_repository

    def ventas_diarias(self, fecha: date) -> ReporteVentasResponse:
        desde = inicio_del_dia(fecha)
        hasta = inicio_del_dia(fecha + timedelta(days=1))

        return ReporteVentasResponse(
            etiqueta_periodo=fecha.isoformat(),
            total_ventas=self.venta_repository.sumar_total_por_estado_y_fecha(EstadoVenta.COMPLETADA, desde, hasta),
            cantidad_transacciones=self.venta_repository.count_by_estado_venta_and_creado_between(
                EstadoVenta.COMPLETADA, desde, hasta
            ),
        )

    def ventas_mensuales(self, mes_ano: AnioMes) -> ReporteVentasResponse:
        desde = inicio_del_dia(mes_ano.at_day(1))
        hasta = inicio_del_dia(mes_ano.plus_months(1).at_day(1))

        return ReporteVentasResponse(
            etiqueta_periodo=str(mes_ano),
            total_ventas=self.venta_repository.sumar_total_por_estado_y_fecha(EstadoVenta.COMPLETADA, desde, hasta),
            cantidad_transacciones=self.venta_repository.count_by_estado_venta_and_creado_between(
                EstadoVenta.COMPLETADA, desde, hasta
            ),
        )

    def productos_mas_vendidos(self, desde: date, hasta: date) -> list[ProductoMasVendidoResponse]:
        desde_fecha_hora = inicio_del_dia(desde)
        hasta_fecha_hora = inicio_del_dia(hasta + timedelta(days=1))

        return [
            ProductoMasVendidoResponse(
                producto_id=p.get_producto_id(),
                nombre_producto=p.get_nombre_producto(),
                cantidad_total_vendida=p.get_cantidad_total(),
            )
            for p in self.detalle_venta_repository.buscar_productos_mas_vendidos(desde_fecha_hora, hasta_fecha_hora)
        ]

    def reporte_inventario(self) -> list[ReporteInventarioItemResponse]:
        return [
            ReporteInventarioItemResponse(
                producto_id=p.id,
                nombre_producto=p.nombre,
                codigo=p.codigo,
                stock_actual=p.stock_actual,
                stock_minimo=p.stock_minimo,
                stock_bajo=p.stock_actual <= p.stock_minimo,
            )
            for p in self.producto_repository.find_all_by_estado_true()
        ]
