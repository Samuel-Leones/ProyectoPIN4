from typing import Optional

from sqlalchemy import select

from app.model.modulo import Modulo
from app.model.modulo_x_rol import ModuloXRol
from app.model.rol import Rol
from app.repository.repositorio_jpa import RepositorioJpa


class ModuloXRolRepository(RepositorioJpa[ModuloXRol]):
    modelo = ModuloXRol

    def find_by_rol_id_and_modulo_id(self, rol_id: int, modulo_id: int) -> Optional[ModuloXRol]:
        consulta = select(ModuloXRol).where(ModuloXRol.rol_id == rol_id, ModuloXRol.modulo_id == modulo_id).limit(1)
        return self.db.scalars(consulta).first()

    def find_all_by_estado_true_and_rol_id(self, rol_id: int) -> list[ModuloXRol]:
        consulta = (
            select(ModuloXRol)
            .where(ModuloXRol.estado.is_(True), ModuloXRol.rol_id == rol_id)
            .order_by(ModuloXRol.id)
        )
        return list(self.db.scalars(consulta).all())

    def find_permiso_activo(self, rol_id: int, ruta_modulo: str) -> Optional[ModuloXRol]:
        """Asignación vigente (rol, módulo) si el rol, el módulo y la asignación están activos."""
        consulta = (
            select(ModuloXRol)
            .join(Modulo, ModuloXRol.modulo_id == Modulo.id)
            .join(Rol, ModuloXRol.rol_id == Rol.id)
            .where(
                ModuloXRol.rol_id == rol_id,
                Modulo.ruta == ruta_modulo,
                ModuloXRol.estado.is_(True),
                Modulo.estado.is_(True),
                Rol.estado.is_(True),
            )
            .limit(1)
        )
        return self.db.scalars(consulta).first()

    def find_modulos_asignados(self, rol_id: int) -> list[ModuloXRol]:
        """Asignaciones vigentes del rol, en el orden de los módulos (para armar el menú)."""
        consulta = (
            select(ModuloXRol)
            .join(Modulo, ModuloXRol.modulo_id == Modulo.id)
            .where(ModuloXRol.rol_id == rol_id, ModuloXRol.estado.is_(True), Modulo.estado.is_(True))
            .order_by(Modulo.id)
        )
        return list(self.db.scalars(consulta).all())
