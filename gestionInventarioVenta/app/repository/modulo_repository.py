from typing import Optional

from sqlalchemy import select

from app.model.modulo import Modulo
from app.repository.repositorio_jpa import RepositorioJpa


class ModuloRepository(RepositorioJpa[Modulo]):
    modelo = Modulo

    def find_by_ruta(self, ruta: str) -> Optional[Modulo]:
        return self.db.scalars(select(Modulo).where(Modulo.ruta == ruta).limit(1)).first()

    def exists_by_nombre_and_id_not(self, nombre: str, id: int) -> bool:
        return self.db.scalar(select(Modulo.id).where(Modulo.nombre == nombre, Modulo.id != id).limit(1)) is not None

    def exists_by_nombre(self, nombre: str) -> bool:
        return self.db.scalar(select(Modulo.id).where(Modulo.nombre == nombre).limit(1)) is not None

    def exists_by_ruta(self, ruta: str) -> bool:
        return self.db.scalar(select(Modulo.id).where(Modulo.ruta == ruta).limit(1)) is not None

    def exists_by_ruta_and_id_not(self, ruta: str, id: int) -> bool:
        return self.db.scalar(select(Modulo.id).where(Modulo.ruta == ruta, Modulo.id != id).limit(1)) is not None
