from sqlalchemy.orm import Session

from app.config.configuracion import configuracion
from app.config.seguridad import CodificadorContrasenas
from app.model.modulo import Modulo
from app.model.modulo_x_rol import ModuloXRol
from app.model.rol import Rol
from app.model.rol_usuario import RolUsuario
from app.model.usuario import Usuario
from app.repository.modulo_repository import ModuloRepository
from app.repository.modulo_x_rol_repository import ModuloXRolRepository
from app.repository.rol_repository import RolRepository
from app.repository.usuario_repository import UsuarioRepository

ROLES = [
    (RolUsuario.SUPER_USUARIO, "Control total del sistema, incluida la seguridad (roles y módulos)"),
    (RolUsuario.ADMINISTRADOR, "Gestiona el negocio, los reportes y los empleados"),
    (RolUsuario.EMPLEADO, "Opera el día a día: ventas, clientes, productos e inventario"),
]

MODULOS = [
    ("Panel", "/panel", "bi-speedometer2", "Estadísticas generales del negocio"),
    ("Productos", "/productos", "bi-box-seam", "Catálogo de productos y alertas de stock"),
    ("Categorías", "/categorias", "bi-tags", "Categorías de productos"),
    ("Proveedores", "/proveedores", "bi-truck", "Proveedores de mercancía"),
    ("Clientes", "/clientes", "bi-people", "Clientes e historial de compras"),
    ("Inventario", "/inventario", "bi-arrow-left-right", "Entradas y salidas de inventario"),
    ("Ventas", "/ventas", "bi-cart-check", "Ventas y facturación"),
    ("Reportes", "/reportes", "bi-bar-chart", "Reportes de ventas e inventario"),
    ("Auditoría", "/auditoria", "bi-shield-lock", "Registro de acciones de los usuarios"),
    ("Usuarios", "/usuarios", "bi-person-gear", "Gestión de usuarios del sistema"),
    ("Seguridad", "/seguridad", "bi-key", "Roles, módulos y permisos"),
]

LECTURA = (False, False, False)
LECTURA_Y_ESCRITURA = (True, True, False)  
TOTAL = (True, True, True)                  

PERMISOS = {
    RolUsuario.EMPLEADO: {
        "/productos": LECTURA_Y_ESCRITURA,
        "/categorias": LECTURA,
        "/proveedores": LECTURA,
        "/clientes": LECTURA_Y_ESCRITURA,
        "/inventario": (True, False, False),
        "/ventas": (True, False, False),
    },
    RolUsuario.ADMINISTRADOR: {
        "/panel": LECTURA,
        "/productos": TOTAL,
        "/categorias": TOTAL,
        "/proveedores": TOTAL,
        "/clientes": TOTAL,
        "/inventario": (True, False, False),
        "/ventas": (True, False, False),
        "/reportes": LECTURA,
        "/auditoria": LECTURA,
        "/usuarios": TOTAL,
    },
    RolUsuario.SUPER_USUARIO: {
        "/panel": LECTURA,
        "/productos": TOTAL,
        "/categorias": TOTAL,
        "/proveedores": TOTAL,
        "/clientes": TOTAL,
        "/inventario": (True, False, False),
        "/ventas": (True, False, False),
        "/reportes": LECTURA,
        "/auditoria": LECTURA,
        "/usuarios": TOTAL,
        "/seguridad": TOTAL,
    },
}


class InicializadorDatos:
    def __init__(
        self,
        rol_repository: RolRepository,
        modulo_repository: ModuloRepository,
        modulo_x_rol_repository: ModuloXRolRepository,
        usuario_repository: UsuarioRepository,
        password_encoder: CodificadorContrasenas,
        correo_semilla: str,
        contrasena_semilla: str,
    ):
        self.rol_repository = rol_repository
        self.modulo_repository = modulo_repository
        self.modulo_x_rol_repository = modulo_x_rol_repository
        self.usuario_repository = usuario_repository
        self.password_encoder = password_encoder
        self.correo_semilla = correo_semilla
        self.contrasena_semilla = contrasena_semilla

    def run(self) -> None:
        roles = self._sembrar_roles()
        modulos = self._sembrar_modulos()
        self._sembrar_permisos(roles, modulos)
        self._sembrar_super_usuario(roles[RolUsuario.SUPER_USUARIO])

    def _sembrar_roles(self) -> dict[str, Rol]:
        roles = {}
        for nombre, descripcion in ROLES:
            rol = self.rol_repository.find_by_nombre(nombre)
            if rol is None:
                rol = self.rol_repository.save(Rol(nombre=nombre, descripcion=descripcion))
            roles[nombre] = rol
        return roles

    def _sembrar_modulos(self) -> dict[str, Modulo]:
        modulos = {}
        for nombre, ruta, icono, descripcion in MODULOS:
            modulo = self.modulo_repository.find_by_ruta(ruta)
            if modulo is None:
                modulo = self.modulo_repository.save(
                    Modulo(nombre=nombre, ruta=ruta, icono=icono, descripcion=descripcion)
                )
            modulos[ruta] = modulo
        return modulos

    def _sembrar_permisos(self, roles: dict[str, Rol], modulos: dict[str, Modulo]) -> None:
        for nombre_rol, permisos in PERMISOS.items():
            for ruta, (crear, editar, eliminar) in permisos.items():
                existente = self.modulo_x_rol_repository.find_by_rol_id_and_modulo_id(
                    roles[nombre_rol].id, modulos[ruta].id
                )
                if existente is None:
                    self.modulo_x_rol_repository.save(
                        ModuloXRol(
                            rol_id=roles[nombre_rol].id,
                            modulo_id=modulos[ruta].id,
                            puede_crear=crear,
                            puede_editar=editar,
                            puede_eliminar=eliminar,
                        )
                    )

    def _sembrar_super_usuario(self, rol_super: Rol) -> None:
        if not self.usuario_repository.exists_by_correo(self.correo_semilla):
            self.usuario_repository.save(
                Usuario(
                    correo=self.correo_semilla,
                    nombre_completo="Super Usuario",
                    contrasena=self.password_encoder.encode(self.contrasena_semilla),
                    rol_id=rol_super.id,
                )
            )


def ejecutar_inicializador(sesion: Session) -> None:
    InicializadorDatos(
        RolRepository(sesion),
        ModuloRepository(sesion),
        ModuloXRolRepository(sesion),
        UsuarioRepository(sesion),
        CodificadorContrasenas(),
        configuracion.semilla_correo,
        configuracion.semilla_contrasena,
    ).run()
