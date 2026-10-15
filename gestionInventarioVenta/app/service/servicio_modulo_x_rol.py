from typing import Optional

from app.dto.base import campos_auditoria
from app.dto.modulo_x_rol.modulo_x_rol_request import ModuloXRolRequest
from app.dto.modulo_x_rol.modulo_x_rol_response import ModuloXRolResponse
from app.dto.modulo_x_rol.modulo_x_rol_update_request import ModuloXRolUpdateRequest
from app.exception.api_exception import RecursoNoEncontradoException
from app.model.accion_auditoria import AccionAuditoria
from app.model.modulo_x_rol import ModuloXRol
from app.repository.modulo_x_rol_repository import ModuloXRolRepository
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_modulo import ServicioModulo
from app.service.servicio_rol import ServicioRol


class ServicioModuloXRol:
    def __init__(
        self,
        modulo_x_rol_repository: ModuloXRolRepository,
        servicio_rol: ServicioRol,
        servicio_modulo: ServicioModulo,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.modulo_x_rol_repository = modulo_x_rol_repository
        self.servicio_rol = servicio_rol
        self.servicio_modulo = servicio_modulo
        self.servicio_auditoria = servicio_auditoria

    def asignar(self, request: ModuloXRolRequest, responsable: str) -> ModuloXRolResponse:
        """Da acceso de un rol a un módulo. Si la asignación existía y estaba eliminada, la reactiva."""
        rol = self.servicio_rol.obtener_entidad_activa_o_lanzar(request.rol_id)
        modulo = self.servicio_modulo.obtener_entidad_activa_o_lanzar(request.modulo_id)

        asignacion = self.modulo_x_rol_repository.find_by_rol_id_and_modulo_id(rol.id, modulo.id)
        if asignacion is None:
            asignacion = ModuloXRol(rol_id=rol.id, modulo_id=modulo.id)
            accion = AccionAuditoria.CREACION
        else:
            accion = AccionAuditoria.ACTUALIZACION

        asignacion.estado = True
        asignacion.puede_crear = request.puede_crear
        asignacion.puede_editar = request.puede_editar
        asignacion.puede_eliminar = request.puede_eliminar

        guardada = self.modulo_x_rol_repository.save(asignacion)
        self.servicio_auditoria.registrar(responsable, accion, "ModuloXRol", guardada.id)
        return self._a_response(guardada)

    def actualizar(self, id: int, request: ModuloXRolUpdateRequest, responsable: str) -> ModuloXRolResponse:
        asignacion = self._buscar_activa_o_lanzar(id)
        asignacion.puede_crear = request.puede_crear
        asignacion.puede_editar = request.puede_editar
        asignacion.puede_eliminar = request.puede_eliminar

        guardada = self.modulo_x_rol_repository.save(asignacion)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "ModuloXRol", id)
        return self._a_response(guardada)

    def eliminar(self, id: int, responsable: str) -> None:
        asignacion = self._buscar_activa_o_lanzar(id)
        asignacion.estado = False  # borrado lógico: el rol pierde el acceso al módulo
        self.modulo_x_rol_repository.save(asignacion)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "ModuloXRol", id)

    def obtener_todas(self, rol_id: Optional[int]) -> list[ModuloXRolResponse]:
        if rol_id is not None:
            asignaciones = self.modulo_x_rol_repository.find_all_by_estado_true_and_rol_id(rol_id)
        else:
            asignaciones = self.modulo_x_rol_repository.find_all_by_estado_true()
        return [self._a_response(a) for a in asignaciones]

    def obtener_por_id(self, id: int) -> ModuloXRolResponse:
        return self._a_response(self._buscar_activa_o_lanzar(id))

    def _buscar_activa_o_lanzar(self, id: int) -> ModuloXRol:
        asignacion = self.modulo_x_rol_repository.find_by_id(id)
        if asignacion is None or not asignacion.estado:
            raise RecursoNoEncontradoException("Asignación de módulo a rol no encontrada")
        return asignacion

    @staticmethod
    def _a_response(a: ModuloXRol) -> ModuloXRolResponse:
        return ModuloXRolResponse(
            id=a.id,
            rol_id=a.rol.id,
            nombre_rol=a.rol.nombre,
            modulo_id=a.modulo.id,
            nombre_modulo=a.modulo.nombre,
            ruta_modulo=a.modulo.ruta,
            puede_crear=a.puede_crear,
            puede_editar=a.puede_editar,
            puede_eliminar=a.puede_eliminar,
            **campos_auditoria(a),
        )
