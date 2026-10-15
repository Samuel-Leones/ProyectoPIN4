from app.dto.base import campos_auditoria
from app.dto.rol.rol_request import RolRequest
from app.dto.rol.rol_response import RolResponse
from app.exception.api_exception import RecursoDuplicadoException, RecursoNoEncontradoException
from app.exception.operacion_no_permitida_exception import OperacionNoPermitidaException
from app.model.accion_auditoria import AccionAuditoria
from app.model.rol import Rol
from app.repository.rol_repository import RolRepository
from app.repository.usuario_repository import UsuarioRepository
from app.service.servicio_auditoria import ServicioAuditoria


class ServicioRol:
    def __init__(
        self,
        rol_repository: RolRepository,
        usuario_repository: UsuarioRepository,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.rol_repository = rol_repository
        self.usuario_repository = usuario_repository
        self.servicio_auditoria = servicio_auditoria

    def crear(self, request: RolRequest, responsable: str) -> RolResponse:
        nombre = request.nombre.strip().upper()
        if self.rol_repository.exists_by_nombre(nombre):
            raise RecursoDuplicadoException("Ya existe un rol con ese nombre")

        rol = Rol(nombre=nombre, descripcion=request.descripcion.strip() if request.descripcion is not None else None)
        guardado = self.rol_repository.save(rol)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "Rol", guardado.id)
        return self._a_response(guardado)

    def actualizar(self, id: int, request: RolRequest, responsable: str) -> RolResponse:
        rol = self._buscar_activo_o_lanzar(id)
        nombre = request.nombre.strip().upper()

        if self.rol_repository.exists_by_nombre_and_id_not(nombre, id):
            raise RecursoDuplicadoException("Ya existe un rol con ese nombre")

        rol.nombre = nombre
        rol.descripcion = request.descripcion.strip() if request.descripcion is not None else None

        guardado = self.rol_repository.save(rol)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Rol", id)
        return self._a_response(guardado)

    def eliminar(self, id: int, responsable: str) -> None:
        rol = self._buscar_activo_o_lanzar(id)

        if self.usuario_repository.exists_by_rol_id_and_estado_true(id):
            raise OperacionNoPermitidaException("No se puede eliminar el rol porque tiene usuarios asignados.")

        rol.estado = False  # borrado lógico
        self.rol_repository.save(rol)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "Rol", id)

    def obtener_todos(self) -> list[RolResponse]:
        return [self._a_response(r) for r in self.rol_repository.find_all_by_estado_true()]

    def obtener_por_id(self, id: int) -> RolResponse:
        return self._a_response(self._buscar_activo_o_lanzar(id))

    def obtener_entidad_activa_o_lanzar(self, id: int) -> Rol:
        return self._buscar_activo_o_lanzar(id)

    def _buscar_activo_o_lanzar(self, id: int) -> Rol:
        rol = self.rol_repository.find_by_id(id)
        if rol is None or not rol.estado:
            raise RecursoNoEncontradoException("Rol no encontrado")
        return rol

    @staticmethod
    def _a_response(rol: Rol) -> RolResponse:
        return RolResponse(id=rol.id, nombre=rol.nombre, descripcion=rol.descripcion, **campos_auditoria(rol))
