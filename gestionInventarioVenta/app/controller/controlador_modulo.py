from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_modulo
from app.config.seguridad import correo_autenticado
from app.dto.modulo.modulo_request import ModuloRequest
from app.dto.modulo.modulo_response import ModuloResponse
from app.service.servicio_modulo import ServicioModulo

router = APIRouter(prefix="/modulos", tags=["Módulos"])


@router.get("", response_model=list[ModuloResponse])
def listar(servicio_modulo: ServicioModulo = Depends(obtener_servicio_modulo)):
    return servicio_modulo.obtener_todos()


@router.get("/{id}", response_model=ModuloResponse)
def obtener(id: int, servicio_modulo: ServicioModulo = Depends(obtener_servicio_modulo)):
    return servicio_modulo.obtener_por_id(id)


@router.post("", response_model=ModuloResponse, status_code=201)
def crear(
    request: ModuloRequest,
    correo: str = Depends(correo_autenticado),
    servicio_modulo: ServicioModulo = Depends(obtener_servicio_modulo),
):
    return servicio_modulo.crear(request, correo)


@router.put("/{id}", response_model=ModuloResponse)
def actualizar(
    id: int,
    request: ModuloRequest,
    correo: str = Depends(correo_autenticado),
    servicio_modulo: ServicioModulo = Depends(obtener_servicio_modulo),
):
    return servicio_modulo.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_modulo: ServicioModulo = Depends(obtener_servicio_modulo),
):
    servicio_modulo.eliminar(id, correo)
    return Response(status_code=204)
