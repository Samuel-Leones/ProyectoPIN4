from typing import Optional

from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_compatibilidad, obtener_servicio_producto
from app.config.seguridad import correo_autenticado
from app.dto.compatibilidad.compatibilidad_request import CompatibilidadRequest
from app.dto.compatibilidad.compatibilidad_response import CompatibilidadResponse
from app.dto.producto.producto_request import ProductoRequest
from app.dto.producto.producto_response import ProductoResponse
from app.dto.tipos import LongOpcional
from app.service.servicio_compatibilidad import ServicioCompatibilidad
from app.service.servicio_producto import ServicioProducto

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("", response_model=list[ProductoResponse])
def listar(
    nombre: Optional[str] = None,
    categoriaId: LongOpcional = None,
    codigo: Optional[str] = None,
    versionMotoId: LongOpcional = None,
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
):
    """Lista los productos; con filtros opcionales. ?versionMotoId=N devuelve los accesorios de esa moto del catálogo."""
    es_busqueda = nombre is not None or categoriaId is not None or codigo is not None or versionMotoId is not None
    if es_busqueda:
        return servicio_producto.buscar(nombre, categoriaId, codigo, versionMotoId)
    return servicio_producto.obtener_todos()


@router.get("/codigo/{codigo}", response_model=ProductoResponse)
def obtener_por_codigo(
    codigo: str,
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
):
    return servicio_producto.obtener_por_codigo(codigo)


@router.get("/bajo-stock", response_model=list[ProductoResponse])
def bajo_stock(servicio_producto: ServicioProducto = Depends(obtener_servicio_producto)):
    return servicio_producto.obtener_bajo_stock()


@router.post("", response_model=ProductoResponse, status_code=201)
def crear(
    request: ProductoRequest,
    correo: str = Depends(correo_autenticado),
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
):
    return servicio_producto.crear(request, correo)


@router.put("/{id}", response_model=ProductoResponse)
def actualizar(
    id: int,
    request: ProductoRequest,
    correo: str = Depends(correo_autenticado),
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
):
    return servicio_producto.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
):
    servicio_producto.eliminar(id, correo)
    return Response(status_code=204)


# ------------------------------------------------------------------ Compatibilidad con motos (servicio externo)
@router.get("/{id}/compatibilidad", response_model=list[CompatibilidadResponse], tags=["Compatibilidad con motos"])
def listar_compatibilidad(
    id: int,
    servicio_compatibilidad: ServicioCompatibilidad = Depends(obtener_servicio_compatibilidad),
):
    """Motos con las que es compatible el producto (se leen de Neon: no consultan el catálogo)."""
    return servicio_compatibilidad.listar(id)


@router.post(
    "/{id}/compatibilidad", response_model=CompatibilidadResponse, status_code=201, tags=["Compatibilidad con motos"]
)
def agregar_compatibilidad(
    id: int,
    request: CompatibilidadRequest,
    correo: str = Depends(correo_autenticado),
    servicio_compatibilidad: ServicioCompatibilidad = Depends(obtener_servicio_compatibilidad),
):
    """Agrega una moto compatible. La versión se valida contra el servicio de catálogo de motos (503 si no responde)."""
    return servicio_compatibilidad.agregar(id, request, correo)


@router.delete("/{id}/compatibilidad/{compatibilidad_id}", status_code=204, tags=["Compatibilidad con motos"])
def quitar_compatibilidad(
    id: int,
    compatibilidad_id: int,
    correo: str = Depends(correo_autenticado),
    servicio_compatibilidad: ServicioCompatibilidad = Depends(obtener_servicio_compatibilidad),
):
    servicio_compatibilidad.quitar(id, compatibilidad_id, correo)
    return Response(status_code=204)
