from http import HTTPStatus


class ApiException(Exception):
    def __init__(self, message: str, status: HTTPStatus):
        super().__init__(message)
        self.message = message
        self.status = status


class RecursoDuplicadoException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.CONFLICT)


class RecursoNoEncontradoException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.NOT_FOUND)


class CredencialesInvalidasException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.UNAUTHORIZED)


class SolicitudInvalidaException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.BAD_REQUEST)


class StockInsuficienteException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.BAD_REQUEST)


class TransicionEstadoInvalidaException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.BAD_REQUEST)


class ServicioNoDisponibleException(ApiException):

    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.SERVICE_UNAVAILABLE)


class AccesoDenegadoException(Exception):
    """Equivalente al 403 que devuelve Spring Security desde el filtro de autorización."""
