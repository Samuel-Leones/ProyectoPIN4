from fastapi import APIRouter, Depends

from app.config.inyeccion import obtener_servicio_factura, obtener_servicio_venta
from app.config.seguridad import correo_autenticado
from app.dto.factura.factura_response import FacturaResponse
from app.dto.venta.venta_request import VentaRequest
from app.dto.venta.venta_response import VentaResponse
from app.service.servicio_factura import ServicioFactura
from app.service.servicio_venta import ServicioVenta

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.post("", response_model=VentaResponse, status_code=201)
def crear(
    request: VentaRequest,
    correo: str = Depends(correo_autenticado),
    servicio_venta: ServicioVenta = Depends(obtener_servicio_venta),
):
    return servicio_venta.crear(request, correo)


@router.get("/{id}", response_model=VentaResponse)
def obtener(id: int, servicio_venta: ServicioVenta = Depends(obtener_servicio_venta)):
    return servicio_venta.obtener_por_id(id)


@router.post("/{id}/completar", response_model=VentaResponse)
def completar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_venta: ServicioVenta = Depends(obtener_servicio_venta),
):
    return servicio_venta.completar(id, correo)


@router.post("/{id}/anular", response_model=VentaResponse)
def anular(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_venta: ServicioVenta = Depends(obtener_servicio_venta),
):
    return servicio_venta.anular(id, correo)


@router.get("/{id}/factura", response_model=FacturaResponse)
def factura(id: int, servicio_factura: ServicioFactura = Depends(obtener_servicio_factura)):
    return servicio_factura.obtener_por_venta_id(id)
