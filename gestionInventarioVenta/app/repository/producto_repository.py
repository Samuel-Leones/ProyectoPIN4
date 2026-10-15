from typing import Optional

from sqlalchemy import func, select

from app.model.producto import Producto
from app.model.producto_compatibilidad import ProductoCompatibilidad
from app.repository.repositorio_jpa import RepositorioJpa


class ProductoRepository(RepositorioJpa[Producto]):
    modelo = Producto

    def exists_by_codigo(self, codigo: str) -> bool:
        return self.db.scalar(select(Producto.id).where(Producto.codigo == codigo).limit(1)) is not None

    def exists_by_codigo_and_id_not(self, codigo: str, id: int) -> bool:
        consulta = select(Producto.id).where(Producto.codigo == codigo, Producto.id != id).limit(1)
        return self.db.scalar(consulta) is not None

    def find_by_codigo_and_estado_true(self, codigo: str) -> Optional[Producto]:
        consulta = select(Producto).where(Producto.codigo == codigo, Producto.estado.is_(True)).limit(1)
        return self.db.scalars(consulta).first()

    def count_by_estado_true_and_stock_actual(self, stock_actual: int) -> int:
        consulta = (
            select(func.count())
            .select_from(Producto)
            .where(Producto.estado.is_(True), Producto.stock_actual == stock_actual)
        )
        return self.db.scalar(consulta) or 0

    def exists_by_categoria_id(self, categoria_id: int) -> bool:
        return self.db.scalar(select(Producto.id).where(Producto.categoria_id == categoria_id).limit(1)) is not None

    def find_all_bajo_stock(self) -> list[Producto]:
        consulta = (
            select(Producto)
            .where(Producto.estado.is_(True), Producto.stock_actual <= Producto.stock_minimo)
            .order_by(Producto.id)
        )
        return list(self.db.scalars(consulta).all())

    def buscar(
        self,
        nombre: Optional[str],
        categoria_id: Optional[int],
        codigo: Optional[str],
        version_moto_id: Optional[int] = None,
    ) -> list[Producto]:
        """Filtros opcionales combinados con AND (LIKE sin escapar, igual que la consulta original)."""
        consulta = select(Producto).where(Producto.estado.is_(True))
        if version_moto_id is not None:
            compatibles = select(ProductoCompatibilidad.producto_id).where(
                ProductoCompatibilidad.version_moto_id == version_moto_id,
                ProductoCompatibilidad.estado.is_(True),
            )
            consulta = consulta.where(Producto.id.in_(compatibles))
        if nombre is not None:
            consulta = consulta.where(func.lower(Producto.nombre).like("%" + func.lower(nombre) + "%"))
        if categoria_id is not None:
            consulta = consulta.where(Producto.categoria_id == categoria_id)
        if codigo is not None:
            consulta = consulta.where(func.lower(Producto.codigo).like("%" + func.lower(codigo) + "%"))
        return list(self.db.scalars(consulta.order_by(Producto.id)).all())
