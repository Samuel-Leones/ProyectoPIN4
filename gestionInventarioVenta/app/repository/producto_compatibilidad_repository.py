from typing import Optional

from sqlalchemy import select

from app.model.producto_compatibilidad import ProductoCompatibilidad
from app.repository.repositorio_jpa import RepositorioJpa


class ProductoCompatibilidadRepository(RepositorioJpa[ProductoCompatibilidad]):
    modelo = ProductoCompatibilidad

    def find_all_by_producto_id_and_estado_true(self, producto_id: int) -> list[ProductoCompatibilidad]:
        consulta = (
            select(ProductoCompatibilidad)
            .where(ProductoCompatibilidad.producto_id == producto_id, ProductoCompatibilidad.estado.is_(True))
            .order_by(ProductoCompatibilidad.id)
        )
        return list(self.db.scalars(consulta).all())

    def find_by_producto_id_and_version_moto_id(
        self, producto_id: int, version_moto_id: int
    ) -> Optional[ProductoCompatibilidad]:
        """Busca la pareja (producto, versión) sin importar el estado: esa pareja es única en la tabla."""
        consulta = (
            select(ProductoCompatibilidad)
            .where(
                ProductoCompatibilidad.producto_id == producto_id,
                ProductoCompatibilidad.version_moto_id == version_moto_id,
            )
            .limit(1)
        )
        return self.db.scalars(consulta).first()
