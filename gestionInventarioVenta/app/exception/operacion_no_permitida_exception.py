from http import HTTPStatus

from app.exception.api_exception import ApiException


class OperacionNoPermitidaException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.CONFLICT)
