from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_rol
from app.config.seguridad import correo_autenticado
from app.dto.rol.rol_request import RolRequest
from app.dto.rol.rol_response import RolResponse
from app.service.servicio_rol import ServicioRol

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=list[RolResponse])
def listar(servicio_rol: ServicioRol = Depends(obtener_servicio_rol)):
    return servicio_rol.obtener_todos()


@router.get("/{id}", response_model=RolResponse)
def obtener(id: int, servicio_rol: ServicioRol = Depends(obtener_servicio_rol)):
    return servicio_rol.obtener_por_id(id)


@router.post("", response_model=RolResponse, status_code=201)
def crear(
    request: RolRequest,
    correo: str = Depends(correo_autenticado),
    servicio_rol: ServicioRol = Depends(obtener_servicio_rol),
):
    return servicio_rol.crear(request, correo)


@router.put("/{id}", response_model=RolResponse)
def actualizar(
    id: int,
    request: RolRequest,
    correo: str = Depends(correo_autenticado),
    servicio_rol: ServicioRol = Depends(obtener_servicio_rol),
):
    return servicio_rol.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_rol: ServicioRol = Depends(obtener_servicio_rol),
):
    servicio_rol.eliminar(id, correo)
    return Response(status_code=204)
