from sqlalchemy import select

from app.model.proveedor import Proveedor
from app.repository.repositorio_jpa import RepositorioJpa


class ProveedorRepository(RepositorioJpa[Proveedor]):
    modelo = Proveedor

    def exists_by_nombre_and_estado_true(self, nombre: str) -> bool:
        consulta = select(Proveedor.id).where(Proveedor.nombre == nombre, Proveedor.estado.is_(True)).limit(1)
        return self.db.scalar(consulta) is not None

    def exists_by_nombre_and_id_not_and_estado_true(self, nombre: str, id: int) -> bool:
        consulta = (
            select(Proveedor.id)
            .where(Proveedor.nombre == nombre, Proveedor.id != id, Proveedor.estado.is_(True))
            .limit(1)
        )
        return self.db.scalar(consulta) is not None
