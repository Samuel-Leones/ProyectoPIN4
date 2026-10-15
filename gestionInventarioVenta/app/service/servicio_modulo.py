from app.dto.base import campos_auditoria
from app.dto.modulo.modulo_request import ModuloRequest
from app.dto.modulo.modulo_response import ModuloResponse
from app.exception.api_exception import RecursoDuplicadoException, RecursoNoEncontradoException
from app.model.accion_auditoria import AccionAuditoria
from app.model.modulo import Modulo
from app.repository.modulo_repository import ModuloRepository
from app.service.servicio_auditoria import ServicioAuditoria


def _limpiar(valor):
    return valor.strip() if valor is not None else None


class ServicioModulo:
    def __init__(self, modulo_repository: ModuloRepository, servicio_auditoria: ServicioAuditoria):
        self.modulo_repository = modulo_repository
        self.servicio_auditoria = servicio_auditoria

    def crear(self, request: ModuloRequest, responsable: str) -> ModuloResponse:
        self._validar_unicos(request.nombre.strip(), request.ruta.strip(), None)

        modulo = Modulo(
            nombre=request.nombre.strip(),
            descripcion=_limpiar(request.descripcion),
            ruta=request.ruta.strip(),
            icono=_limpiar(request.icono),
        )
        guardado = self.modulo_repository.save(modulo)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "Modulo", guardado.id)
        return self._a_response(guardado)

    def actualizar(self, id: int, request: ModuloRequest, responsable: str) -> ModuloResponse:
        modulo = self._buscar_activo_o_lanzar(id)
        self._validar_unicos(request.nombre.strip(), request.ruta.strip(), id)

        modulo.nombre = request.nombre.strip()
        modulo.descripcion = _limpiar(request.descripcion)
        modulo.ruta = request.ruta.strip()
        modulo.icono = _limpiar(request.icono)

        guardado = self.modulo_repository.save(modulo)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Modulo", id)
        return self._a_response(guardado)

    def eliminar(self, id: int, responsable: str) -> None:
        modulo = self._buscar_activo_o_lanzar(id)
        modulo.estado = False  # borrado lógico
        self.modulo_repository.save(modulo)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "Modulo", id)

    def obtener_todos(self) -> list[ModuloResponse]:
        return [self._a_response(m) for m in self.modulo_repository.find_all_by_estado_true()]

    def obtener_por_id(self, id: int) -> ModuloResponse:
        return self._a_response(self._buscar_activo_o_lanzar(id))

    def obtener_entidad_activa_o_lanzar(self, id: int) -> Modulo:
        return self._buscar_activo_o_lanzar(id)

    def _validar_unicos(self, nombre: str, ruta: str, id_actual) -> None:
        if id_actual is None:
            nombre_repetido = self.modulo_repository.exists_by_nombre(nombre)
            ruta_repetida = self.modulo_repository.exists_by_ruta(ruta)
        else:
            nombre_repetido = self.modulo_repository.exists_by_nombre_and_id_not(nombre, id_actual)
            ruta_repetida = self.modulo_repository.exists_by_ruta_and_id_not(ruta, id_actual)
        if nombre_repetido:
            raise RecursoDuplicadoException("Ya existe un módulo con ese nombre")
        if ruta_repetida:
            raise RecursoDuplicadoException("Ya existe un módulo con esa ruta")

    def _buscar_activo_o_lanzar(self, id: int) -> Modulo:
        modulo = self.modulo_repository.find_by_id(id)
        if modulo is None or not modulo.estado:
            raise RecursoNoEncontradoException("Módulo no encontrado")
        return modulo

    @staticmethod
    def _a_response(modulo: Modulo) -> ModuloResponse:
        return ModuloResponse(
            id=modulo.id,
            nombre=modulo.nombre,
            descripcion=modulo.descripcion,
            ruta=modulo.ruta,
            icono=modulo.icono,
            **campos_auditoria(modulo),
        )
