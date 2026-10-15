from sqlalchemy import select

from app.model.categoria import Categoria
from app.repository.repositorio_jpa import RepositorioJpa


class CategoriaRepository(RepositorioJpa[Categoria]):
    modelo = Categoria

    def exists_by_nombre_and_estado_true(self, nombre: str) -> bool:
        consulta = select(Categoria.id).where(Categoria.nombre == nombre, Categoria.estado.is_(True)).limit(1)
        return self.db.scalar(consulta) is not None

    def exists_by_nombre_and_id_not_and_estado_true(self, nombre: str, id: int) -> bool:
        consulta = (
            select(Categoria.id)
            .where(Categoria.nombre == nombre, Categoria.id != id, Categoria.estado.is_(True))
            .limit(1)
        )
        return self.db.scalar(consulta) is not None
