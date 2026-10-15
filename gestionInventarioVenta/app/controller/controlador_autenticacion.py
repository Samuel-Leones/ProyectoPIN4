from fastapi import APIRouter, Depends

from app.config.inyeccion import obtener_servicio_autenticacion
from app.config.seguridad import correo_autenticado
from app.dto.autenticacion.login_request import LoginRequest
from app.dto.autenticacion.modulo_asignado_response import ModuloAsignadoResponse
from app.dto.autenticacion.registro_request import RegistroRequest
from app.dto.autenticacion.token_response import TokenResponse
from app.dto.autenticacion.usuario_response import UsuarioResponse
from app.service.servicio_autenticacion import ServicioAutenticacion

router = APIRouter(prefix="/autenticacion", tags=["Autenticación"])


@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registrar(
    request: RegistroRequest,
    correo: str = Depends(correo_autenticado),
    servicio_autenticacion: ServicioAutenticacion = Depends(obtener_servicio_autenticacion),
):
    return servicio_autenticacion.registrar(request, correo)


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    servicio_autenticacion: ServicioAutenticacion = Depends(obtener_servicio_autenticacion),
):
    return servicio_autenticacion.login(request)


@router.get("/mis-modulos", response_model=list[ModuloAsignadoResponse])
def mis_modulos(
    correo: str = Depends(correo_autenticado),
    servicio_autenticacion: ServicioAutenticacion = Depends(obtener_servicio_autenticacion),
):
    """Módulos a los que puede entrar el rol del usuario autenticado (sirve para armar el menú)."""
    return servicio_autenticacion.obtener_mis_modulos(correo)
