from typing import Optional

from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_modulo_x_rol
from app.config.seguridad import correo_autenticado
from app.dto.modulo_x_rol.modulo_x_rol_request import ModuloXRolRequest
from app.dto.modulo_x_rol.modulo_x_rol_response import ModuloXRolResponse
from app.dto.modulo_x_rol.modulo_x_rol_update_request import ModuloXRolUpdateRequest
from app.dto.tipos import LongOpcional
from app.service.servicio_modulo_x_rol import ServicioModuloXRol

router = APIRouter(prefix="/modulos-roles", tags=["Módulos por rol"])


@router.get("", response_model=list[ModuloXRolResponse])
def listar(
    rolId: LongOpcional = None,
    servicio: ServicioModuloXRol = Depends(obtener_servicio_modulo_x_rol),
):
    """Asignaciones vigentes; con ?rolId=N solo las de ese rol."""
    return servicio.obtener_todas(rolId)


@router.get("/{id}", response_model=ModuloXRolResponse)
def obtener(id: int, servicio: ServicioModuloXRol = Depends(obtener_servicio_modulo_x_rol)):
    return servicio.obtener_por_id(id)


@router.post("", response_model=ModuloXRolResponse, status_code=201)
def asignar(
    request: ModuloXRolRequest,
    correo: str = Depends(correo_autenticado),
    servicio: ServicioModuloXRol = Depends(obtener_servicio_modulo_x_rol),
):
    """Da a un rol acceso a un módulo (si estaba revocado, lo reactiva)."""
    return servicio.asignar(request, correo)


@router.put("/{id}", response_model=ModuloXRolResponse)
def actualizar(
    id: int,
    request: ModuloXRolUpdateRequest,
    correo: str = Depends(correo_autenticado),
    servicio: ServicioModuloXRol = Depends(obtener_servicio_modulo_x_rol),
):
    return servicio.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def revocar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio: ServicioModuloXRol = Depends(obtener_servicio_modulo_x_rol),
):
    """Quita al rol el acceso al módulo (borrado lógico)."""
    servicio.eliminar(id, correo)
    return Response(status_code=204)
