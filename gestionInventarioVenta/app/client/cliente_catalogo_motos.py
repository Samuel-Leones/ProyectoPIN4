import logging
from dataclasses import dataclass

import httpx

from app.config.configuracion import configuracion
from app.exception.api_exception import RecursoNoEncontradoException, ServicioNoDisponibleException

logger = logging.getLogger("app.client.cliente_catalogo_motos")

MENSAJE_NO_DISPONIBLE = "El servicio de catálogo de motos no está disponible. Intenta de nuevo más tarde."

@dataclass(frozen=True)
class VersionMoto:
    id: int
    marca: str
    modelo: str
    anio: int
    cilindraje: int
    descripcion: str 


class ClienteCatalogoMotos:
    def __init__(self, url_base: str, timeout_segundos: float):
        self.url_base = url_base.rstrip("/")
        self.timeout_segundos = timeout_segundos

    def obtener_version(self, version_id: int) -> VersionMoto:
    
        url = f"{self.url_base}/versiones/{version_id}"
        try:
            respuesta = httpx.get(url, timeout=self.timeout_segundos, headers={"Accept": "application/json"})
        except (httpx.HTTPError, httpx.InvalidURL) as error:
            logger.warning("No se pudo consultar el catálogo de motos en %s: %s", url, error)
            raise ServicioNoDisponibleException(MENSAJE_NO_DISPONIBLE) from error

        if respuesta.status_code in (400, 404):
            raise RecursoNoEncontradoException("Versión de moto no encontrada en el catálogo")
        if respuesta.status_code != 200:
            logger.warning("El catálogo de motos respondió %s a %s", respuesta.status_code, url)
            raise ServicioNoDisponibleException(MENSAJE_NO_DISPONIBLE)

        try:
            datos = respuesta.json()
            return VersionMoto(
                id=int(datos["id"]),
                marca=str(datos["nombreMarca"]),
                modelo=str(datos["nombreModelo"]),
                anio=int(datos["anio"]),
                cilindraje=int(datos["cilindraje"]),
                descripcion=str(datos["descripcion"]),
            )
        except (ValueError, KeyError, TypeError) as error:
            logger.warning("Respuesta inesperada del catálogo de motos en %s: %s", url, error)
            raise ServicioNoDisponibleException("El servicio de catálogo de motos devolvió una respuesta inesperada") from error


def crear_cliente_catalogo_motos() -> ClienteCatalogoMotos:
    return ClienteCatalogoMotos(configuracion.catalogo_motos_url, configuracion.catalogo_motos_timeout)
