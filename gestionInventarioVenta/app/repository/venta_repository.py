from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, func, select

from app.model.estado_venta import EstadoVenta
from app.model.venta import Venta
from app.repository.repositorio_jpa import RepositorioJpa


class VentaRepository(RepositorioJpa[Venta]):
    modelo = Venta

    def find_all_by_cliente_id_order_by_creado_desc(self, cliente_id: int) -> list[Venta]:
        consulta = select(Venta).where(Venta.cliente_id == cliente_id).order_by(Venta.creado.desc(), Venta.id.desc())
        return list(self.db.scalars(consulta).all())

    def exists_by_cliente_id(self, cliente_id: int) -> bool:
        return self.db.scalar(select(Venta.id).where(Venta.cliente_id == cliente_id).limit(1)) is not None

    def count_by_estado_venta_and_creado_between(self, estado_venta: EstadoVenta, desde: datetime, hasta: datetime) -> int:
        """Rango [desde, hasta): incluye 'desde' y excluye 'hasta'."""
        consulta = (
            select(func.count())
            .select_from(Venta)
            .where(Venta.estado_venta == estado_venta, Venta.creado >= desde, Venta.creado < hasta)
        )
        return self.db.scalar(consulta) or 0

    def sumar_total_por_estado_y_fecha(self, estado_venta: EstadoVenta, desde: datetime, hasta: datetime) -> Decimal:
        consulta = select(func.coalesce(func.sum(Venta.total), 0).cast(Numeric(38, 2))).where(
            Venta.estado_venta == estado_venta, Venta.creado >= desde, Venta.creado < hasta
        )
        resultado = self.db.scalar(consulta)
        return Decimal(str(resultado if resultado is not None else 0))
