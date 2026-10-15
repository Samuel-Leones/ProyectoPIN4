from app.dto.base import campos_auditoria
from app.dto.categoria.categoria_request import CategoriaRequest
from app.dto.categoria.categoria_response import CategoriaResponse
from app.dto.categoria.categoria_update_request import CategoriaUpdateRequest
from app.exception.api_exception import RecursoDuplicadoException, RecursoNoEncontradoException
from app.model.accion_auditoria import AccionAuditoria
from app.model.categoria import Categoria
from app.repository.categoria_repository import CategoriaRepository
from app.service.servicio_auditoria import ServicioAuditoria


class ServicioCategoria:
    def __init__(self, categoria_repository: CategoriaRepository, servicio_auditoria: ServicioAuditoria):
        self.categoria_repository = categoria_repository
        self.servicio_auditoria = servicio_auditoria

    def crear(self, request: CategoriaRequest, responsable: str) -> CategoriaResponse:
        if self.categoria_repository.exists_by_nombre_and_estado_true(request.nombre.strip()):
            raise RecursoDuplicadoException("Ya existe una categoría con ese nombre")

        categoria = Categoria(
            nombre=request.nombre.strip(),
            descripcion=request.descripcion.strip() if request.descripcion is not None else None,
        )

        guardada = self.categoria_repository.save(categoria)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "Categoria", guardada.id)
        return self._a_response(guardada)

    def actualizar(self, id: int, request: CategoriaUpdateRequest, responsable: str) -> CategoriaResponse:
        categoria = self._buscar_por_id_o_lanzar(id)

        if request.nombre is not None:
            nuevo_nombre = request.nombre.strip()

            if self.categoria_repository.exists_by_nombre_and_id_not_and_estado_true(nuevo_nombre, id):
                raise RecursoDuplicadoException("Ya existe una categoría con ese nombre")

            categoria.nombre = nuevo_nombre

        if request.descripcion is not None:
            categoria.descripcion = request.descripcion.strip()

        guardada = self.categoria_repository.save(categoria)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Categoria", id)
        return self._a_response(guardada)

    def eliminar(self, id: int, responsable: str) -> None:
        categoria = self._buscar_por_id_o_lanzar(id)

        # Borrado lógico: el registro no se borra, solo cambia su estado a false.
        categoria.estado = False
        self.categoria_repository.save(categoria)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "Categoria", id)

    def obtener_todas(self) -> list[CategoriaResponse]:
        return [self._a_response(c) for c in self.categoria_repository.find_all_by_estado_true()]

    def obtener_por_id_o_lanzar(self, id: int) -> Categoria:
        return self._buscar_por_id_o_lanzar(id)

    def _buscar_por_id_o_lanzar(self, id: int) -> Categoria:
        categoria = self.categoria_repository.find_by_id(id)
        if categoria is None or not categoria.estado:
            raise RecursoNoEncontradoException("Categoría no encontrada")
        return categoria

    @staticmethod
    def _a_response(categoria: Categoria) -> CategoriaResponse:
        return CategoriaResponse(
            id=categoria.id,
            nombre=categoria.nombre,
            descripcion=categoria.descripcion,
            **campos_auditoria(categoria),
        )
