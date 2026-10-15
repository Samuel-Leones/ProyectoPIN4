from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from zoneinfo import ZoneInfo

from pydantic import BeforeValidator, PlainSerializer

from app.config.configuracion import configuracion


def formatear_fecha_hora(valor: datetime) -> str:
    if valor.tzinfo is not None:
        valor = valor.astimezone(ZoneInfo(configuracion.zona_horaria))
    return valor.isoformat()


def _a_numero(valor: Decimal) -> float:
    return float(valor)


FechaHora = Annotated[datetime, PlainSerializer(formatear_fecha_hora, return_type=str)]

Dinero = Annotated[Decimal, PlainSerializer(_a_numero, return_type=float)]


def _vacio_a_none(valor):
    return None if valor == "" else valor


LongOpcional = Annotated[Optional[int], BeforeValidator(_vacio_a_none)]
