from fastapi import APIRouter, Depends, Response

from app.config.inyeccion import obtener_servicio_categoria
from app.config.seguridad import correo_autenticado
from app.dto.categoria.categoria_request import CategoriaRequest
from app.dto.categoria.categoria_response import CategoriaResponse
from app.dto.categoria.categoria_update_request import CategoriaUpdateRequest
from app.service.servicio_categoria import ServicioCategoria

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("", response_model=list[CategoriaResponse])
def listar(servicio_categoria: ServicioCategoria = Depends(obtener_servicio_categoria)):
    return servicio_categoria.obtener_todas()


@router.post("", response_model=CategoriaResponse, status_code=201)
def crear(
    request: CategoriaRequest,
    correo: str = Depends(correo_autenticado),
    servicio_categoria: ServicioCategoria = Depends(obtener_servicio_categoria),
):
    return servicio_categoria.crear(request, correo)


@router.put("/{id}", response_model=CategoriaResponse)
def actualizar(
    id: int,
    request: CategoriaUpdateRequest,
    correo: str = Depends(correo_autenticado),
    servicio_categoria: ServicioCategoria = Depends(obtener_servicio_categoria),
):
    return servicio_categoria.actualizar(id, request, correo)


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    correo: str = Depends(correo_autenticado),
    servicio_categoria: ServicioCategoria = Depends(obtener_servicio_categoria),
):
    servicio_categoria.eliminar(id, correo)
    return Response(status_code=204)
