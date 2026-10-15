from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_usuario
from app.config.seguridad import correo_autenticado
from app.dto.autenticacion.usuario_response import UsuarioResponse
from app.dto.usuario.usuario_update_request import UsuarioUpdateRequest
from app.service.servicio_usuario import ServicioUsuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[UsuarioResponse])
def listar(servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario)):
    return servicio_usuario.obtener_todos()


@router.get("/{id}", response_model=UsuarioResponse)
def obtener(id: int, servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario)):
    return servicio_usuario.obtener_por_id(id)


@router.put("/{id}", response_model=UsuarioResponse)
def actualizar(
    id: int,
    request: UsuarioUpdateRequest,
    correo: str = Depends(correo_autenticado),
    servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario),
):
    return servicio_usuario.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario),
):
    servicio_usuario.eliminar(id, correo)
    return Response(status_code=204)
