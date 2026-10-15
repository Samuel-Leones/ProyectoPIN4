from typing import Optional

from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_cliente, obtener_servicio_venta
from app.config.seguridad import correo_autenticado
from app.dto.cliente.cliente_request import ClienteRequest
from app.dto.cliente.cliente_response import ClienteResponse
from app.dto.cliente.cliente_update_request import ClienteUpdateRequest
from app.dto.venta.venta_response import VentaResponse
from app.service.servicio_cliente import ServicioCliente
from app.service.servicio_venta import ServicioVenta

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("", response_model=list[ClienteResponse])
def listar(
    buscar: Optional[str] = None,
    servicio_cliente: ServicioCliente = Depends(obtener_servicio_cliente),
):
    if buscar is None or buscar.strip() == "":
        return servicio_cliente.obtener_todos()
    return servicio_cliente.buscar(buscar)


@router.post("", response_model=ClienteResponse, status_code=201)
def crear(
    request: ClienteRequest,
    correo: str = Depends(correo_autenticado),
    servicio_cliente: ServicioCliente = Depends(obtener_servicio_cliente),
):
    return servicio_cliente.crear(request, correo)


@router.put("/{id}", response_model=ClienteResponse)
def actualizar(
    id: int,
    request: ClienteUpdateRequest,
    correo: str = Depends(correo_autenticado),
    servicio_cliente: ServicioCliente = Depends(obtener_servicio_cliente),
):
    return servicio_cliente.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_cliente: ServicioCliente = Depends(obtener_servicio_cliente),
):
    servicio_cliente.eliminar(id, correo)
    return Response(status_code=204)


@router.get("/{id}/compras", response_model=list[VentaResponse])
def historial_compras(
    id: int,
    servicio_venta: ServicioVenta = Depends(obtener_servicio_venta),
):
    return servicio_venta.obtener_historial_compras(id)
