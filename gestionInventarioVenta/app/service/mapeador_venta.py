"""Mapper compartido entre ServicioVenta y ServicioFactura para evitar una dependencia circular."""
from decimal import Decimal

from app.dto.base import campos_auditoria
from app.dto.venta.detalle_venta_response import DetalleVentaResponse
from app.dto.venta.venta_response import VentaResponse
from app.model.venta import Venta


def a_venta_response(venta: Venta) -> VentaResponse:
    return VentaResponse(
        id=venta.id,
        cliente_id=venta.cliente.id,
        nombre_cliente=venta.cliente.nombre,
        vendedor_id=venta.vendedor.id,
        correo_vendedor=venta.vendedor.correo,
        subtotal=venta.subtotal,
        iva=venta.iva,
        total=venta.total,
        estado_venta=venta.estado_venta,
        detalles=[
            DetalleVentaResponse(
                producto_id=d.producto.id,
                nombre_producto=d.producto.nombre,
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario,
                total_linea=d.precio_unitario * Decimal(d.cantidad),
            )
            for d in venta.detalles
        ],
        **campos_auditoria(venta),
    )
