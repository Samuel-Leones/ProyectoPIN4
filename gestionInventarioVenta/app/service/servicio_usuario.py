from app.config.seguridad import CodificadorContrasenas
from app.dto.autenticacion.usuario_response import UsuarioResponse
from app.dto.usuario.usuario_update_request import UsuarioUpdateRequest
from app.exception.api_exception import CredencialesInvalidasException, RecursoNoEncontradoException
from app.exception.operacion_no_permitida_exception import OperacionNoPermitidaException
from app.model.accion_auditoria import AccionAuditoria
from app.model.usuario import Usuario
from app.repository.rol_repository import RolRepository
from app.repository.usuario_repository import UsuarioRepository
from app.service.politica_roles import puede_gestionar
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_autenticacion import ServicioAutenticacion


class ServicioUsuario:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        rol_repository: RolRepository,
        password_encoder: CodificadorContrasenas,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.usuario_repository = usuario_repository
        self.rol_repository = rol_repository
        self.password_encoder = password_encoder
        self.servicio_auditoria = servicio_auditoria

    def obtener_todos(self) -> list[UsuarioResponse]:
        return [ServicioAutenticacion.a_response(u) for u in self.usuario_repository.find_all_by_estado_true()]

    def obtener_por_id(self, id: int) -> UsuarioResponse:
        return ServicioAutenticacion.a_response(self._buscar_activo_o_lanzar(id))

    def actualizar(self, id: int, request: UsuarioUpdateRequest, responsable: str) -> UsuarioResponse:
        actor = self._buscar_actor(responsable)
        usuario = self._buscar_activo_o_lanzar(id)
        self._validar_permiso(actor, usuario)

        if request.nombre_completo is not None:
            usuario.nombre_completo = request.nombre_completo.strip()

        if request.rol_id is not None:
            rol = self.rol_repository.find_by_id(request.rol_id)
            if rol is None or not rol.estado:
                raise RecursoNoEncontradoException("Rol no encontrado")
            if not puede_gestionar(actor.rol.nombre, rol.nombre):
                raise OperacionNoPermitidaException(
                    f"El rol {actor.rol.nombre} no tiene permiso para asignar el rol {rol.nombre}"
                )
            usuario.rol_id = rol.id
            usuario.rol = rol

        if request.contrasena is not None:
            usuario.contrasena = self.password_encoder.encode(request.contrasena)

        guardado = self.usuario_repository.save(usuario)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Usuario", id)
        return ServicioAutenticacion.a_response(guardado)

    def eliminar(self, id: int, responsable: str) -> None:
        actor = self._buscar_actor(responsable)
        usuario = self._buscar_activo_o_lanzar(id)
        self._validar_permiso(actor, usuario)

        usuario.estado = False  # borrado lógico
        self.usuario_repository.save(usuario)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "Usuario", id)

    @staticmethod
    def _validar_permiso(actor: Usuario, objetivo: Usuario) -> None:
        if not puede_gestionar(actor.rol.nombre, objetivo.rol.nombre):
            raise OperacionNoPermitidaException(
                f"El rol {actor.rol.nombre} no tiene permiso para modificar usuarios con rol {objetivo.rol.nombre}"
            )

    def _buscar_actor(self, correo: str) -> Usuario:
        actor = self.usuario_repository.find_by_correo(correo)
        if actor is None:
            raise CredencialesInvalidasException("Usuario no encontrado")
        return actor

    def _buscar_activo_o_lanzar(self, id: int) -> Usuario:
        usuario = self.usuario_repository.find_by_id(id)
        if usuario is None or not usuario.estado:
            raise RecursoNoEncontradoException("Usuario no encontrado")
        return usuario
