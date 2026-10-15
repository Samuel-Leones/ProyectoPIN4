from decimal import ROUND_HALF_UP, Decimal

from app.dto.venta.venta_request import VentaRequest
from app.dto.venta.venta_response import VentaResponse
from app.exception.api_exception import (
    CredencialesInvalidasException,
    RecursoNoEncontradoException,
    TransicionEstadoInvalidaException,
)
from app.model.accion_auditoria import AccionAuditoria
from app.model.detalle_venta import DetalleVenta
from app.model.estado_venta import EstadoVenta
from app.model.tipo_movimiento_inventario import TipoMovimientoInventario
from app.model.venta import Venta
from app.repository.usuario_repository import UsuarioRepository
from app.repository.venta_repository import VentaRepository
from app.service.mapeador_venta import a_venta_response
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_cliente import ServicioCliente
from app.service.servicio_factura import ServicioFactura
from app.service.servicio_inventario import ServicioInventario
from app.service.servicio_producto import ServicioProducto

TASA_IVA = Decimal("0.19")
DOS_DECIMALES = Decimal("0.01")


class ServicioVenta:
    def __init__(
        self,
        venta_repository: VentaRepository,
        servicio_cliente: ServicioCliente,
        servicio_producto: ServicioProducto,
        usuario_repository: UsuarioRepository,
        servicio_inventario: ServicioInventario,
        servicio_factura: ServicioFactura,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.venta_repository = venta_repository
        self.servicio_cliente = servicio_cliente
        self.servicio_producto = servicio_producto
        self.usuario_repository = usuario_repository
        self.servicio_inventario = servicio_inventario
        self.servicio_factura = servicio_factura
        self.servicio_auditoria = servicio_auditoria

    def crear(self, request: VentaRequest, responsable: str) -> VentaResponse:
        cliente = self.servicio_cliente.obtener_por_id_o_lanzar(request.cliente_id)
        vendedor = self.usuario_repository.find_by_correo(responsable)
        if vendedor is None:
            raise CredencialesInvalidasException("Usuario no encontrado")

        subtotal = Decimal(0)
        detalles: list[DetalleVenta] = []

        venta = Venta(
            cliente=cliente,
            vendedor=vendedor,
            subtotal=Decimal(0),
            iva=Decimal(0),
            total=Decimal(0),
        )

        for item in request.items:
            producto = self.servicio_producto.obtener_entidad_activa_o_lanzar(item.producto_id)
            total_linea = producto.precio * Decimal(item.cantidad)
            subtotal = subtotal + total_linea

            detalles.append(
                DetalleVenta(
                    venta=venta,
                    producto=producto,
                    cantidad=item.cantidad,
                    precio_unitario=producto.precio,
                )
            )

        iva = (subtotal * TASA_IVA).quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)
        total = subtotal + iva

        venta.subtotal = subtotal.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)
        venta.iva = iva
        venta.total = total
        venta.detalles = detalles

        guardada = self.venta_repository.save(venta)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "Venta", guardada.id)
        return a_venta_response(guardada)

    def completar(self, id: int, responsable: str) -> VentaResponse:
        """Confirma la venta: descuenta stock (RF-04) y genera la factura (RF-07)."""
        venta = self._buscar_por_id_o_lanzar(id)

        if venta.estado_venta != EstadoVenta.PENDIENTE:
            raise TransicionEstadoInvalidaException("Solo una venta pendiente puede completarse")

        for detalle in venta.detalles:
            self.servicio_inventario.aplicar_cambio_stock(
                producto=detalle.producto,
                cantidad=detalle.cantidad,
                tipo=TipoMovimientoInventario.SALIDA,
                motivo=f"Venta #{venta.id}",
                responsable=responsable,
            )

        venta.estado_venta = EstadoVenta.COMPLETADA
        guardada = self.venta_repository.save(venta)
        self.servicio_factura.generar_para_venta(guardada)

        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Venta", id)
        return a_venta_response(guardada)

    def anular(self, id: int, responsable: str) -> VentaResponse:
        venta = self._buscar_por_id_o_lanzar(id)

        if venta.estado_venta != EstadoVenta.PENDIENTE:
            raise TransicionEstadoInvalidaException("Solo una venta pendiente puede anularse")

        venta.estado_venta = EstadoVenta.ANULADA
        guardada = self.venta_repository.save(venta)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Venta", id)
        return a_venta_response(guardada)

    def obtener_por_id(self, id: int) -> VentaResponse:
        return a_venta_response(self._buscar_por_id_o_lanzar(id))

    def obtener_historial_compras(self, cliente_id: int) -> list[VentaResponse]:
        self.servicio_cliente.obtener_por_id_o_lanzar(cliente_id)
        ventas = self.venta_repository.find_all_by_cliente_id_order_by_creado_desc(cliente_id)
        return [a_venta_response(v) for v in ventas]

    def _buscar_por_id_o_lanzar(self, id: int) -> Venta:
        venta = self.venta_repository.find_by_id(id)
        if venta is None:
            raise RecursoNoEncontradoException("Venta no encontrada")
        return venta
