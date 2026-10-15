import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse, Response

from app.exception.api_error import crear_api_error
from app.exception.api_exception import AccesoDenegadoException, ApiException

logger = logging.getLogger("app.exception.global_exception_handler")


def _responder(estado: HTTPStatus, mensaje: str, ruta: str) -> JSONResponse:
    cuerpo = crear_api_error(estado, mensaje, ruta).a_dict()
    return JSONResponse(status_code=estado.value, content=cuerpo)


def _ruta_del_campo(loc: tuple) -> str:
    texto = ""
    for parte in loc[1:]:
        if isinstance(parte, int):
            texto += f"[{parte}]"
        else:
            texto += f".{parte}" if texto else str(parte)
    return texto


async def manejar_api_exception(request: Request, ex: ApiException) -> JSONResponse:
    return _responder(ex.status, ex.message or "Error inesperado", request.url.path)


async def manejar_validacion(request: Request, ex: RequestValidationError) -> JSONResponse:
    errores = ex.errors()

    if any(e["loc"] and e["loc"][0] in ("query", "path") for e in errores):
        return _responder(HTTPStatus.INTERNAL_SERVER_ERROR, "Error interno del servidor", request.url.path)

    if any(e["type"] != "value_error" for e in errores):
        return _responder(
            HTTPStatus.BAD_REQUEST, "Cuerpo de la solicitud inválido o incompleto", request.url.path
        )

    mensaje = "; ".join(
        f"{_ruta_del_campo(e['loc'])}: {e['ctx']['error']}" for e in errores
    )
    return _responder(HTTPStatus.BAD_REQUEST, mensaje, request.url.path)


async def manejar_acceso_denegado(request: Request, ex: AccesoDenegadoException) -> Response:
    return Response(status_code=403)


async def manejar_http_exception(request: Request, ex: StarletteHTTPException) -> JSONResponse:
    try:
        estado = HTTPStatus(ex.status_code)
    except ValueError:
        estado = HTTPStatus.INTERNAL_SERVER_ERROR
    return _responder(estado, str(ex.detail), request.url.path)


class CapturaExcepcionesInesperadasMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        respuesta_iniciada = False

        async def enviar_controlado(mensaje):
            nonlocal respuesta_iniciada
            if mensaje["type"] == "http.response.start":
                respuesta_iniciada = True
            await send(mensaje)

        try:
            await self.app(scope, receive, enviar_controlado)
        except Exception:
            ruta = scope.get("path", "")
            logger.exception("Error inesperado en %s", ruta)
            if respuesta_iniciada:
                raise
            respuesta = _responder(HTTPStatus.INTERNAL_SERVER_ERROR, "Error interno del servidor", ruta)
            await respuesta(scope, receive, send)


def registrar_manejadores(app: FastAPI) -> None:
    app.add_exception_handler(ApiException, manejar_api_exception)
    app.add_exception_handler(RequestValidationError, manejar_validacion)
    app.add_exception_handler(AccesoDenegadoException, manejar_acceso_denegado)
    app.add_exception_handler(StarletteHTTPException, manejar_http_exception)
    app.add_middleware(CapturaExcepcionesInesperadasMiddleware)
