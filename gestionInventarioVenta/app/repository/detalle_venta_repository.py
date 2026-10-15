from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, select

from app.model.detalle_venta import DetalleVenta
from app.model.estado_venta import EstadoVenta
from app.model.producto import Producto
from app.model.venta import Venta
from app.repository.repositorio_jpa import RepositorioJpa


@dataclass(frozen=True)
class ProductoMasVendidoProjection:
    producto_id: int
    nombre_producto: str
    cantidad_total: int

    def get_producto_id(self) -> int:
        return self.producto_id

    def get_nombre_producto(self) -> str:
        return self.nombre_producto

    def get_cantidad_total(self) -> int:
        return self.cantidad_total


class DetalleVentaRepository(RepositorioJpa[DetalleVenta]):
    modelo = DetalleVenta

    def buscar_productos_mas_vendidos(self, desde: datetime, hasta: datetime) -> list[ProductoMasVendidoProjection]:
        cantidad_total = func.sum(DetalleVenta.cantidad)
        consulta = (
            select(Producto.id, Producto.nombre, cantidad_total.label("cantidad_total"))
            .select_from(DetalleVenta)
            .join(Venta, DetalleVenta.venta_id == Venta.id)
            .join(Producto, DetalleVenta.producto_id == Producto.id)
            .where(Venta.estado_venta == EstadoVenta.COMPLETADA, Venta.creado >= desde, Venta.creado < hasta)
            .group_by(Producto.id, Producto.nombre)
            .order_by(cantidad_total.desc(), Producto.id)
        )
        return [
            ProductoMasVendidoProjection(int(fila[0]), fila[1], int(fila[2]))
            for fila in self.db.execute(consulta).all()
        ]
