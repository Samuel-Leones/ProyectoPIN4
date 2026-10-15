from typing import Optional

from sqlalchemy import select

from app.model.rol import Rol
from app.repository.repositorio_jpa import RepositorioJpa


class RolRepository(RepositorioJpa[Rol]):
    modelo = Rol

    def find_by_nombre(self, nombre: str) -> Optional[Rol]:
        return self.db.scalars(select(Rol).where(Rol.nombre == nombre).limit(1)).first()

    def exists_by_nombre(self, nombre: str) -> bool:
        return self.db.scalar(select(Rol.id).where(Rol.nombre == nombre).limit(1)) is not None

    def exists_by_nombre_and_id_not(self, nombre: str, id: int) -> bool:
        return self.db.scalar(select(Rol.id).where(Rol.nombre == nombre, Rol.id != id).limit(1)) is not None
