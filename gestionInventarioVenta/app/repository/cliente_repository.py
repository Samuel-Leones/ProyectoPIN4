from sqlalchemy import func, or_, select

from app.model.cliente import Cliente
from app.repository.repositorio_jpa import RepositorioJpa


class ClienteRepository(RepositorioJpa[Cliente]):
    modelo = Cliente

    def exists_by_documento_and_estado_true(self, documento: str) -> bool:
        consulta = select(Cliente.id).where(Cliente.documento == documento, Cliente.estado.is_(True)).limit(1)
        return self.db.scalar(consulta) is not None

    def exists_by_documento_and_id_not_and_estado_true(self, documento: str, id: int) -> bool:
        consulta = (
            select(Cliente.id)
            .where(Cliente.documento == documento, Cliente.id != id, Cliente.estado.is_(True))
            .limit(1)
        )
        return self.db.scalar(consulta) is not None

    def buscar_activos(self, termino: str) -> list[Cliente]:
        consulta = (
            select(Cliente)
            .where(
                Cliente.estado.is_(True),
                or_(
                    func.lower(Cliente.nombre).contains(termino.lower(), autoescape=True),
                    func.lower(Cliente.documento).contains(termino.lower(), autoescape=True),
                ),
            )
            .order_by(Cliente.id)
        )
        return list(self.db.scalars(consulta).all())
