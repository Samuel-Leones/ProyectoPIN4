import enum


class TipoMovimientoInventario(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
