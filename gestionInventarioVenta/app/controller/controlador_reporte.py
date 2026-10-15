from datetime import date

from fastapi import APIRouter, Depends

from app.config.inyeccion import obtener_servicio_reporte
from app.dto.reporte.producto_mas_vendido_response import ProductoMasVendidoResponse
from app.dto.reporte.reporte_inventario_item_response import ReporteInventarioItemResponse
from app.dto.reporte.reporte_ventas_response import ReporteVentasResponse
from app.service.servicio_reporte import ServicioReporte
from app.util.anio_mes import AnioMes

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/ventas-diarias", response_model=ReporteVentasResponse)
def ventas_diarias(
    fecha: date,
    servicio_reporte: ServicioReporte = Depends(obtener_servicio_reporte),
):
    return servicio_reporte.ventas_diarias(fecha)


@router.get("/ventas-mensuales", response_model=ReporteVentasResponse)
def ventas_mensuales(
    anio: int,
    mes: int,
    servicio_reporte: ServicioReporte = Depends(obtener_servicio_reporte),
):
    return servicio_reporte.ventas_mensuales(AnioMes.of(anio, mes))


@router.get("/productos-mas-vendidos", response_model=list[ProductoMasVendidoResponse])
def productos_mas_vendidos(
    desde: date,
    hasta: date,
    servicio_reporte: ServicioReporte = Depends(obtener_servicio_reporte),
):
    return servicio_reporte.productos_mas_vendidos(desde, hasta)


@router.get("/inventario", response_model=list[ReporteInventarioItemResponse])
def inventario(servicio_reporte: ServicioReporte = Depends(obtener_servicio_reporte)):
    return servicio_reporte.reporte_inventario()
