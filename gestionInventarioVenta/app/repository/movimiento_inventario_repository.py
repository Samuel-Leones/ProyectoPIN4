from sqlalchemy import select

from app.model.movimiento_inventario import MovimientoInventario
from app.repository.repositorio_jpa import RepositorioJpa


class MovimientoInventarioRepository(RepositorioJpa[MovimientoInventario]):
    modelo = MovimientoInventario

    def find_all_by_producto_id_order_by_creado_desc(self, producto_id: int) -> list[MovimientoInventario]:
        consulta = (
            select(MovimientoInventario)
            .where(MovimientoInventario.producto_id == producto_id)
            .order_by(MovimientoInventario.creado.desc(), MovimientoInventario.id.desc())
        )
        return list(self.db.scalars(consulta).all())
