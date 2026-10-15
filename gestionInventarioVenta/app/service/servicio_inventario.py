from typing import Optional

from app.dto.base import campos_auditoria
from app.dto.inventario.movimiento_inventario_request import MovimientoInventarioRequest
from app.dto.inventario.movimiento_inventario_response import MovimientoInventarioResponse
from app.exception.api_exception import CredencialesInvalidasException, StockInsuficienteException
from app.model.accion_auditoria import AccionAuditoria
from app.model.movimiento_inventario import MovimientoInventario
from app.model.producto import Producto
from app.model.tipo_movimiento_inventario import TipoMovimientoInventario
from app.repository.movimiento_inventario_repository import MovimientoInventarioRepository
from app.repository.usuario_repository import UsuarioRepository
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_producto import ServicioProducto


class ServicioInventario:
    def __init__(
        self,
        movimiento_inventario_repository: MovimientoInventarioRepository,
        servicio_producto: ServicioProducto,
        usuario_repository: UsuarioRepository,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.movimiento_inventario_repository = movimiento_inventario_repository
        self.servicio_producto = servicio_producto
        self.usuario_repository = usuario_repository
        self.servicio_auditoria = servicio_auditoria

    def registrar_movimiento(
        self, request: MovimientoInventarioRequest, responsable: str
    ) -> MovimientoInventarioResponse:
        producto = self.servicio_producto.obtener_entidad_activa_o_lanzar(request.producto_id)
        movimiento = self.aplicar_cambio_stock(producto, request.cantidad, request.tipo, request.motivo, responsable)
        return self._a_response(movimiento)

    def aplicar_cambio_stock(
        self,
        producto: Producto,
        cantidad: int,
        tipo: TipoMovimientoInventario,
        motivo: Optional[str],
        responsable: str,
    ) -> MovimientoInventario:
        if tipo == TipoMovimientoInventario.ENTRADA:
            nuevo_stock = producto.stock_actual + cantidad
        else:
            nuevo_stock = producto.stock_actual - cantidad

        if nuevo_stock < 0:
            raise StockInsuficienteException(
                f"Stock insuficiente para el producto '{producto.nombre}'. "
                f"Disponible: {producto.stock_actual}, solicitado: {cantidad}"
            )

        producto.stock_actual = nuevo_stock
        self.servicio_producto.guardar(producto)

        usuario = self.usuario_repository.find_by_correo(responsable)
        if usuario is None:
            raise CredencialesInvalidasException("Usuario no encontrado")

        movimiento = MovimientoInventario(
            producto=producto,
            tipo=tipo,
            cantidad=cantidad,
            motivo=motivo,
            usuario=usuario,
        )

        guardado = self.movimiento_inventario_repository.save(movimiento)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "MovimientoInventario", guardado.id)
        return guardado

    def obtener_movimientos_por_producto(self, producto_id: int) -> list[MovimientoInventarioResponse]:
        movimientos = self.movimiento_inventario_repository.find_all_by_producto_id_order_by_creado_desc(producto_id)
        return [self._a_response(m) for m in movimientos]

    @staticmethod
    def _a_response(movimiento: MovimientoInventario) -> MovimientoInventarioResponse:
        return MovimientoInventarioResponse(
            id=movimiento.id,
            producto_id=movimiento.producto.id,
            nombre_producto=movimiento.producto.nombre,
            tipo=movimiento.tipo,
            cantidad=movimiento.cantidad,
            motivo=movimiento.motivo,
            stock_resultante=movimiento.producto.stock_actual,
            correo_usuario=movimiento.usuario.correo,
            **campos_auditoria(movimiento),
        )
