from app.dto.base import DtoAuditoria


class CompatibilidadResponse(DtoAuditoria):
    id: int
    producto_id: int
    version_moto_id: int
    descripcion_moto: str
