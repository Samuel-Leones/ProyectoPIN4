from typing import Optional

import bcrypt
from fastapi import Depends, FastAPI, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.config.base_datos import obtener_sesion
from app.config.openapi import esquema_bearer
from app.exception.api_exception import AccesoDenegadoException, CredencialesInvalidasException
from app.repository.modulo_x_rol_repository import ModuloXRolRepository
from app.repository.usuario_repository import UsuarioRepository
from app.service.servicio_jwt import obtener_servicio_jwt


class CodificadorContrasenas:

    @staticmethod
    def _bytes(valor: str) -> bytes:
        return valor.encode("utf-8")[:72] 

    def encode(self, contrasena: str) -> str:
        return bcrypt.hashpw(self._bytes(contrasena), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("utf-8")

    def matches(self, contrasena: str, hash_guardado: str) -> bool:
        try:
            return bcrypt.checkpw(self._bytes(contrasena), hash_guardado.encode("utf-8"))
        except ValueError:
            return False


def obtener_codificador_contrasenas() -> CodificadorContrasenas:
    return CodificadorContrasenas()


def configurar_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
        allow_credentials=True,
    )


PREFIJOS_MODULO: list[tuple[str, str]] = [
    ("/autenticacion/registro", "/usuarios"),
    ("/panel", "/panel"),
    ("/productos", "/productos"),
    ("/categorias", "/categorias"),
    ("/proveedores", "/proveedores"),
    ("/clientes", "/clientes"),
    ("/inventario", "/inventario"),
    ("/ventas", "/ventas"),
    ("/reportes", "/reportes"),
    ("/auditoria", "/auditoria"),
    ("/usuarios", "/usuarios"),
    ("/roles", "/seguridad"),
    ("/modulos", "/seguridad"),
    ("/modulos-roles", "/seguridad"),
]


def _coincide(prefijo: str, ruta: str) -> bool:
    return ruta == prefijo or ruta.startswith(prefijo + "/")


def _modulo_de_la_ruta(ruta: str) -> Optional[str]:
    for prefijo, modulo in PREFIJOS_MODULO:
        if _coincide(prefijo, ruta):
            return modulo
    return None


def _accion_permitida(metodo: str, permiso) -> bool:
    if metodo in ("GET", "HEAD", "OPTIONS"):
        return True  
    if metodo == "POST":
        return permiso.puede_crear
    if metodo in ("PUT", "PATCH"):
        return permiso.puede_editar
    if metodo == "DELETE":
        return permiso.puede_eliminar
    return False


def _autenticar_con_jwt(request: Request, db: Session):
    encabezado = request.headers.get("Authorization")
    if encabezado is None or not encabezado.startswith("Bearer "):
        return None

    token = encabezado.removeprefix("Bearer ").strip()
    servicio_jwt = obtener_servicio_jwt()
    correo = servicio_jwt.extraer_correo(token)

    if correo is not None and servicio_jwt.es_token_valido(token):
        usuario = UsuarioRepository(db).find_by_correo(correo)
        if usuario is not None and usuario.estado and usuario.rol.estado:
            request.state.correo = usuario.correo
            return usuario
    return None


def autorizar_solicitud(
    request: Request,
    _credenciales=Security(esquema_bearer), 
    db: Session = Depends(obtener_sesion),
) -> None:
    ruta = request.url.path
    metodo = request.method

    if metodo == "POST" and ruta == "/autenticacion/login":
        return 

    usuario = _autenticar_con_jwt(request, db)
    if usuario is None:
        raise AccesoDenegadoException()

    ruta_modulo = _modulo_de_la_ruta(ruta)
    if ruta_modulo is None:
        return  

    permiso = ModuloXRolRepository(db).find_permiso_activo(usuario.rol_id, ruta_modulo)
    if permiso is None or not _accion_permitida(metodo, permiso):
        raise AccesoDenegadoException()


def correo_autenticado(request: Request) -> str:
    correo = getattr(request.state, "correo", None)
    if correo is None:
        raise CredencialesInvalidasException("No autorizado")
    return correo


def respuesta_acceso_denegado() -> Response:
    return Response(status_code=403)
