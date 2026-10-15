from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_proveedor
from app.config.seguridad import correo_autenticado
from app.dto.proveedor.proveedor_request import ProveedorRequest
from app.dto.proveedor.proveedor_response import ProveedorResponse
from app.service.servicio_proveedor import ServicioProveedor

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.get("", response_model=list[ProveedorResponse])
def listar(servicio_proveedor: ServicioProveedor = Depends(obtener_servicio_proveedor)):
    return servicio_proveedor.obtener_todos()


@router.post("", response_model=ProveedorResponse, status_code=201)
def crear(
    request: ProveedorRequest,
    correo: str = Depends(correo_autenticado),
    servicio_proveedor: ServicioProveedor = Depends(obtener_servicio_proveedor),
):
    return servicio_proveedor.crear(request, correo)


@router.put("/{id}", response_model=ProveedorResponse)
def actualizar(
    id: int,
    request: ProveedorRequest,
    correo: str = Depends(correo_autenticado),
    servicio_proveedor: ServicioProveedor = Depends(obtener_servicio_proveedor),
):
    return servicio_proveedor.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_proveedor: ServicioProveedor = Depends(obtener_servicio_proveedor),
):
    servicio_proveedor.eliminar(id, correo)
    return Response(status_code=204)
