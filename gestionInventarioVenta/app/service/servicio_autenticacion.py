from app.config.seguridad import CodificadorContrasenas
from app.dto.autenticacion.login_request import LoginRequest
from app.dto.autenticacion.modulo_asignado_response import ModuloAsignadoResponse
from app.dto.autenticacion.registro_request import RegistroRequest
from app.dto.autenticacion.token_response import TokenResponse
from app.dto.autenticacion.usuario_response import UsuarioResponse
from app.dto.base import campos_auditoria
from app.exception.api_exception import (
    CredencialesInvalidasException,
    RecursoDuplicadoException,
    RecursoNoEncontradoException,
)
from app.exception.operacion_no_permitida_exception import OperacionNoPermitidaException
from app.model.accion_auditoria import AccionAuditoria
from app.model.usuario import Usuario
from app.repository.modulo_x_rol_repository import ModuloXRolRepository
from app.repository.rol_repository import RolRepository
from app.repository.usuario_repository import UsuarioRepository
from app.service.politica_roles import puede_gestionar
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_jwt import ServicioJwt


class ServicioAutenticacion:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        rol_repository: RolRepository,
        modulo_x_rol_repository: ModuloXRolRepository,
        password_encoder: CodificadorContrasenas,
        servicio_jwt: ServicioJwt,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.usuario_repository = usuario_repository
        self.rol_repository = rol_repository
        self.modulo_x_rol_repository = modulo_x_rol_repository
        self.password_encoder = password_encoder
        self.servicio_jwt = servicio_jwt
        self.servicio_auditoria = servicio_auditoria

    def registrar(self, request: RegistroRequest, correo_creador: str) -> UsuarioResponse:
        creador = self._buscar_usuario_por_correo(correo_creador)

        rol = self.rol_repository.find_by_id(request.rol_id)
        if rol is None or not rol.estado:
            raise RecursoNoEncontradoException("Rol no encontrado")

        if not puede_gestionar(creador.rol.nombre, rol.nombre):
            raise OperacionNoPermitidaException(
                f"El rol {creador.rol.nombre} no tiene permiso para crear usuarios con rol {rol.nombre}"
            )

        correo = request.correo.strip().lower()
        if self.usuario_repository.exists_by_correo(correo):
            raise RecursoDuplicadoException("El correo ya se encuentra registrado")

        usuario = Usuario(
            correo=correo,
            nombre_completo=request.nombre_completo.strip(),
            contrasena=self.password_encoder.encode(request.contrasena),
            rol_id=rol.id,
        )

        guardado = self.usuario_repository.save(usuario)
        self.servicio_auditoria.registrar(correo_creador, AccionAuditoria.CREACION, "Usuario", guardado.id)
        return self.a_response(guardado)

    def login(self, request: LoginRequest) -> TokenResponse:
        correo = request.correo.strip().lower()

        # Usuario inexistente, eliminado (estado = false), con rol desactivado o contraseña incorrecta
        # => "Credenciales inválidas".
        usuario = self.usuario_repository.find_by_correo(correo)
        if (
            usuario is None
            or not usuario.estado
            or not usuario.rol.estado
            or not self.password_encoder.matches(request.contrasena, usuario.contrasena)
        ):
            raise CredencialesInvalidasException("Credenciales inválidas")

        token = self.servicio_jwt.generar_token(usuario)

        return TokenResponse(
            token_acceso=token,
            expira_en_segundos=self.servicio_jwt.minutos_expiracion * 60,
        )

    def obtener_mis_modulos(self, correo: str) -> list[ModuloAsignadoResponse]:
        """Módulos a los que puede entrar el rol del usuario autenticado (para armar el menú)."""
        usuario = self._buscar_usuario_por_correo(correo)
        return [
            ModuloAsignadoResponse(
                modulo_id=a.modulo.id,
                nombre=a.modulo.nombre,
                descripcion=a.modulo.descripcion,
                ruta=a.modulo.ruta,
                icono=a.modulo.icono,
                puede_crear=a.puede_crear,
                puede_editar=a.puede_editar,
                puede_eliminar=a.puede_eliminar,
            )
            for a in self.modulo_x_rol_repository.find_modulos_asignados(usuario.rol_id)
        ]

    def _buscar_usuario_por_correo(self, correo: str) -> Usuario:
        usuario = self.usuario_repository.find_by_correo(correo)
        if usuario is None:
            raise CredencialesInvalidasException("Usuario no encontrado")
        return usuario

    @staticmethod
    def a_response(usuario: Usuario) -> UsuarioResponse:
        return UsuarioResponse(
            id=usuario.id,
            correo=usuario.correo,
            nombre_completo=usuario.nombre_completo,
            rol_id=usuario.rol.id,
            rol=usuario.rol.nombre,
            **campos_auditoria(usuario),
        )
