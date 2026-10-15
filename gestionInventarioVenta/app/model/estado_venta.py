import enum


class EstadoVenta(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    COMPLETADA = "COMPLETADA"
    ANULADA = "ANULADA"
