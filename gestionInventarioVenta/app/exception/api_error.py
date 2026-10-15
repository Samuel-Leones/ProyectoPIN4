from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus

from app.dto.tipos import formatear_fecha_hora


@dataclass
class ApiError:
    status: int
    error: str
    message: str
    path: str
    timestamp: datetime = field(default_factory=datetime.now)

    def a_dict(self) -> dict:
        return {
            "timestamp": formatear_fecha_hora(self.timestamp),
            "status": self.status,
            "error": self.error,
            "message": self.message,
            "path": self.path,
        }


def crear_api_error(estado: HTTPStatus, mensaje: str, ruta: str) -> ApiError:
    return ApiError(status=estado.value, error=estado.phrase, message=mensaje, path=ruta)
