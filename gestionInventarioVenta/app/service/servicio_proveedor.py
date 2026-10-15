from app.dto.base import campos_auditoria
from app.dto.proveedor.proveedor_request import ProveedorRequest
from app.dto.proveedor.proveedor_response import ProveedorResponse
from app.exception.api_exception import RecursoDuplicadoException, RecursoNoEncontradoException
from app.model.accion_auditoria import AccionAuditoria
from app.model.proveedor import Proveedor
from app.repository.proveedor_repository import ProveedorRepository
from app.service.servicio_auditoria import ServicioAuditoria


def _limpiar(valor):
    return valor.strip() if valor is not None else None


class ServicioProveedor:
    def __init__(self, proveedor_repository: ProveedorRepository, servicio_auditoria: ServicioAuditoria):
        self.proveedor_repository = proveedor_repository
        self.servicio_auditoria = servicio_auditoria

    def crear(self, request: ProveedorRequest, responsable: str) -> ProveedorResponse:
        if self.proveedor_repository.exists_by_nombre_and_estado_true(request.nombre.strip()):
            raise RecursoDuplicadoException("Ya existe un proveedor con ese nombre")

        proveedor = Proveedor(
            nombre=request.nombre.strip(),
            nombre_contacto=_limpiar(request.nombre_contacto),
            telefono=_limpiar(request.telefono),
            correo=request.correo.strip().lower() if request.correo is not None else None,
        )

        guardado = self.proveedor_repository.save(proveedor)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "Proveedor", guardado.id)
        return self._a_response(guardado)

    def actualizar(self, id: int, request: ProveedorRequest, responsable: str) -> ProveedorResponse:
        proveedor = self._buscar_por_id_o_lanzar(id)

        if self.proveedor_repository.exists_by_nombre_and_id_not_and_estado_true(request.nombre.strip(), id):
            raise RecursoDuplicadoException("Ya existe un proveedor con ese nombre")

        proveedor.nombre = request.nombre.strip()
        proveedor.nombre_contacto = _limpiar(request.nombre_contacto)
        proveedor.telefono = _limpiar(request.telefono)
        proveedor.correo = request.correo.strip().lower() if request.correo is not None else None

        guardado = self.proveedor_repository.save(proveedor)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Proveedor", id)
        return self._a_response(guardado)

    def eliminar(self, id: int, responsable: str) -> None:
        proveedor = self._buscar_por_id_o_lanzar(id)
        proveedor.estado = False  # borrado lógico
        self.proveedor_repository.save(proveedor)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "Proveedor", id)

    def obtener_todos(self) -> list[ProveedorResponse]:
        return [self._a_response(p) for p in self.proveedor_repository.find_all_by_estado_true()]

    def obtener_por_id_o_lanzar(self, id: int) -> Proveedor:
        return self._buscar_por_id_o_lanzar(id)

    def _buscar_por_id_o_lanzar(self, id: int) -> Proveedor:
        proveedor = self.proveedor_repository.find_by_id(id)
        if proveedor is None or not proveedor.estado:
            raise RecursoNoEncontradoException("Proveedor no encontrado")
        return proveedor

    @staticmethod
    def _a_response(proveedor: Proveedor) -> ProveedorResponse:
        return ProveedorResponse(
            id=proveedor.id,
            nombre=proveedor.nombre,
            nombre_contacto=proveedor.nombre_contacto,
            telefono=proveedor.telefono,
            correo=proveedor.correo,
            **campos_auditoria(proveedor),
        )
