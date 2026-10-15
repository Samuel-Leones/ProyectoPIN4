from typing import Optional

from sqlalchemy import select

from app.model.factura import Factura
from app.repository.repositorio_jpa import RepositorioJpa


class FacturaRepository(RepositorioJpa[Factura]):
    modelo = Factura

    def find_by_venta_id(self, venta_id: int) -> Optional[Factura]:
        return self.db.scalars(select(Factura).where(Factura.venta_id == venta_id).limit(1)).first()

    def exists_by_numero_factura(self, numero_factura: str) -> bool:
        consulta = select(Factura.id).where(Factura.numero_factura == numero_factura).limit(1)
        return self.db.scalar(consulta) is not None
