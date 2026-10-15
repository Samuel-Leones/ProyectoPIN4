from typing import Optional

from fastapi import APIRouter, Depends

from app.config.inyeccion import obtener_servicio_auditoria
from app.dto.auditoria.registro_auditoria_response import RegistroAuditoriaResponse
from app.service.servicio_auditoria import ServicioAuditoria

router = APIRouter(prefix="/auditoria", tags=["Auditoría"])


@router.get("", response_model=list[RegistroAuditoriaResponse])
def listar(
    entidad: Optional[str] = None,
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
):
    return servicio_auditoria.obtener_registros(entidad)
