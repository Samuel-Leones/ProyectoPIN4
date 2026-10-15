from app.dto.base import campos_auditoria
from app.dto.cliente.cliente_request import ClienteRequest
from app.dto.cliente.cliente_response import ClienteResponse
from app.dto.cliente.cliente_update_request import ClienteUpdateRequest
from app.exception.api_exception import RecursoDuplicadoException, RecursoNoEncontradoException
from app.exception.operacion_no_permitida_exception import OperacionNoPermitidaException
from app.model.accion_auditoria import AccionAuditoria
from app.model.cliente import Cliente
from app.repository.cliente_repository import ClienteRepository
from app.repository.venta_repository import VentaRepository
from app.service.servicio_auditoria import ServicioAuditoria


class ServicioCliente:
    def __init__(
        self,
        cliente_repository: ClienteRepository,
        venta_repository: VentaRepository,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.cliente_repository = cliente_repository
        self.venta_repository = venta_repository
        self.servicio_auditoria = servicio_auditoria

    def crear(self, request: ClienteRequest, responsable: str) -> ClienteResponse:
        if self.cliente_repository.exists_by_documento_and_estado_true(request.documento.strip()):
            raise RecursoDuplicadoException("Ya existe un cliente con ese documento")

        cliente = Cliente(
            nombre=request.nombre.strip(),
            documento=request.documento.strip(),
            telefono=request.telefono.strip() if request.telefono is not None else None,
            correo=request.correo.strip().lower() if request.correo is not None else None,
            direccion=request.direccion.strip() if request.direccion is not None else None,
        )

        guardado = self.cliente_repository.save(cliente)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "Cliente", guardado.id)
        return self._a_response(guardado)

    def actualizar(self, id: int, request: ClienteUpdateRequest, responsable: str) -> ClienteResponse:
        cliente = self._buscar_por_id_o_lanzar(id)

        if request.documento is not None:
            nuevo_documento = request.documento.strip()

            if self.cliente_repository.exists_by_documento_and_id_not_and_estado_true(nuevo_documento, id):
                raise RecursoDuplicadoException("Ya existe un cliente con ese documento")

            cliente.documento = nuevo_documento

        if request.nombre is not None:
            cliente.nombre = request.nombre.strip()

        if request.telefono is not None:
            cliente.telefono = request.telefono.strip()

        if request.correo is not None:
            cliente.correo = request.correo.strip().lower()

        if request.direccion is not None:
            cliente.direccion = request.direccion.strip()

        guardado = self.cliente_repository.save(cliente)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Cliente", id)
        return self._a_response(guardado)

    def eliminar(self, id: int, responsable: str) -> None:
        cliente = self._buscar_por_id_o_lanzar(id)

        if self.venta_repository.exists_by_cliente_id(id):
            raise OperacionNoPermitidaException("No se puede eliminar el cliente porque tiene ventas registradas.")

        cliente.estado = False  # borrado lógico
        self.cliente_repository.save(cliente)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "Cliente", id)

    def obtener_todos(self) -> list[ClienteResponse]:
        return [self._a_response(c) for c in self.cliente_repository.find_all_by_estado_true()]

    def buscar(self, termino: str) -> list[ClienteResponse]:
        return [self._a_response(c) for c in self.cliente_repository.buscar_activos(termino)]

    def obtener_por_id_o_lanzar(self, id: int) -> Cliente:
        return self._buscar_por_id_o_lanzar(id)

    def _buscar_por_id_o_lanzar(self, id: int) -> Cliente:
        cliente = self.cliente_repository.find_by_id(id)
        if cliente is None or not cliente.estado:
            raise RecursoNoEncontradoException("Cliente no encontrado")
        return cliente

    @staticmethod
    def _a_response(cliente: Cliente) -> ClienteResponse:
        return ClienteResponse(
            id=cliente.id,
            nombre=cliente.nombre,
            documento=cliente.documento,
            telefono=cliente.telefono,
            correo=cliente.correo,
            direccion=cliente.direccion,
            **campos_auditoria(cliente),
        )
