from fastapi import APIRouter, Depends

from app.config.inyeccion import obtener_servicio_inventario
from app.config.seguridad import correo_autenticado
from app.dto.inventario.movimiento_inventario_request import MovimientoInventarioRequest
from app.dto.inventario.movimiento_inventario_response import MovimientoInventarioResponse
from app.service.servicio_inventario import ServicioInventario

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.post("/movimientos", response_model=MovimientoInventarioResponse, status_code=201)
def registrar(
    request: MovimientoInventarioRequest,
    correo: str = Depends(correo_autenticado),
    servicio_inventario: ServicioInventario = Depends(obtener_servicio_inventario),
):
    return servicio_inventario.registrar_movimiento(request, correo)


@router.get("/movimientos/producto/{producto_id}", response_model=list[MovimientoInventarioResponse])
def historial(
    producto_id: int,
    servicio_inventario: ServicioInventario = Depends(obtener_servicio_inventario),
):
    return servicio_inventario.obtener_movimientos_por_producto(producto_id)
