import enum


class AccionAuditoria(str, enum.Enum):
    CREACION = "CREACION"
    ACTUALIZACION = "ACTUALIZACION"
    ELIMINACION = "ELIMINACION"
