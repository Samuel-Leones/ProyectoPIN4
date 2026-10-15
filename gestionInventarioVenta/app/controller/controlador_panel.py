from fastapi import APIRouter, Depends

from app.config.inyeccion import obtener_servicio_panel
from app.dto.panel.estadisticas_panel_response import EstadisticasPanelResponse
from app.service.servicio_panel import ServicioPanel

router = APIRouter(prefix="/panel", tags=["Panel"])


@router.get("/estadisticas", response_model=EstadisticasPanelResponse)
def estadisticas(servicio_panel: ServicioPanel = Depends(obtener_servicio_panel)):
    return servicio_panel.obtener_estadisticas()
