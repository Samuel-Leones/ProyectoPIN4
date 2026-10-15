from typing import Optional

from app.dto.base import campos_auditoria
from app.dto.producto.producto_request import ProductoRequest
from app.dto.producto.producto_response import ProductoResponse
from app.exception.api_exception import RecursoDuplicadoException, RecursoNoEncontradoException
from app.model.accion_auditoria import AccionAuditoria
from app.model.producto import Producto
from app.repository.producto_repository import ProductoRepository
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_categoria import ServicioCategoria
from app.service.servicio_proveedor import ServicioProveedor


def _vacio_a_none(valor: Optional[str]) -> Optional[str]:
    return None if valor is None or valor.strip() == "" else valor


class ServicioProducto:
    def __init__(
        self,
        producto_repository: ProductoRepository,
        servicio_categoria: ServicioCategoria,
        servicio_proveedor: ServicioProveedor,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.producto_repository = producto_repository
        self.servicio_categoria = servicio_categoria
        self.servicio_proveedor = servicio_proveedor
        self.servicio_auditoria = servicio_auditoria

    def crear(self, request: ProductoRequest, responsable: str) -> ProductoResponse:
        if self.producto_repository.exists_by_codigo(request.codigo.strip()):
            raise RecursoDuplicadoException("Ya existe un producto con ese código")

        categoria = self.servicio_categoria.obtener_por_id_o_lanzar(request.categoria_id)
        proveedor = (
            self.servicio_proveedor.obtener_por_id_o_lanzar(request.proveedor_id)
            if request.proveedor_id is not None
            else None
        )

        producto = Producto(
            nombre=request.nombre.strip(),
            descripcion=request.descripcion.strip() if request.descripcion is not None else None,
            codigo=request.codigo.strip(),
            categoria=categoria,
            proveedor=proveedor,
            precio=request.precio,
            stock_actual=request.stock_inicial,
            stock_minimo=request.stock_minimo,
        )

        guardado = self.producto_repository.save(producto)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.CREACION, "Producto", guardado.id)
        return self._a_response(guardado)

    def actualizar(self, id: int, request: ProductoRequest, responsable: str) -> ProductoResponse:
        producto = self._buscar_activo_o_lanzar(id)

        if self.producto_repository.exists_by_codigo_and_id_not(request.codigo.strip(), id):
            raise RecursoDuplicadoException("Ya existe un producto con ese código")

        producto.nombre = request.nombre.strip()
        producto.descripcion = request.descripcion.strip() if request.descripcion is not None else None
        producto.codigo = request.codigo.strip()
        producto.categoria = self.servicio_categoria.obtener_por_id_o_lanzar(request.categoria_id)
        producto.proveedor = (
            self.servicio_proveedor.obtener_por_id_o_lanzar(request.proveedor_id)
            if request.proveedor_id is not None
            else None
        )
        producto.precio = request.precio
        producto.stock_minimo = request.stock_minimo

        guardado = self.producto_repository.save(producto)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ACTUALIZACION, "Producto", id)
        return self._a_response(guardado)

    def eliminar(self, id: int, responsable: str) -> None:
        producto = self._buscar_activo_o_lanzar(id)
        producto.estado = False  # borrado lógico
        self.producto_repository.save(producto)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "Producto", id)

    def obtener_todos(self) -> list[ProductoResponse]:
        return [self._a_response(p) for p in self.producto_repository.find_all_by_estado_true()]

    def obtener_por_codigo(self, codigo: str) -> ProductoResponse:
        producto = self.producto_repository.find_by_codigo_and_estado_true(codigo)
        if producto is None:
            raise RecursoNoEncontradoException("Producto no encontrado")
        return self._a_response(producto)

    def buscar(
        self,
        nombre: Optional[str],
        categoria_id: Optional[int],
        codigo: Optional[str],
        version_moto_id: Optional[int] = None,
    ) -> list[ProductoResponse]:
        productos = self.producto_repository.buscar(
            _vacio_a_none(nombre.strip() if nombre is not None else None),
            categoria_id,
            _vacio_a_none(codigo.strip() if codigo is not None else None),
            version_moto_id,
        )
        return [self._a_response(p) for p in productos]

    def obtener_bajo_stock(self) -> list[ProductoResponse]:
        return [self._a_response(p) for p in self.producto_repository.find_all_bajo_stock()]

    def obtener_entidad_activa_o_lanzar(self, id: int) -> Producto:
        return self._buscar_activo_o_lanzar(id)

    def guardar(self, producto: Producto) -> Producto:
        return self.producto_repository.save(producto)

    def _buscar_activo_o_lanzar(self, id: int) -> Producto:
        producto = self.producto_repository.find_by_id(id)
        if producto is None or not producto.estado:
            raise RecursoNoEncontradoException("Producto no encontrado")
        return producto

    def _a_response(self, producto: Producto) -> ProductoResponse:
        return ProductoResponse(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            codigo=producto.codigo,
            categoria_id=producto.categoria.id,
            nombre_categoria=producto.categoria.nombre,
            proveedor_id=producto.proveedor.id if producto.proveedor is not None else None,
            nombre_proveedor=producto.proveedor.nombre if producto.proveedor is not None else None,
            precio=producto.precio,
            stock_actual=producto.stock_actual,
            stock_minimo=producto.stock_minimo,
            stock_bajo=producto.stock_actual <= producto.stock_minimo,
            mensaje_alerta=self._generar_mensaje_alerta(producto.stock_actual, producto.stock_minimo, producto.nombre),
            **campos_auditoria(producto),
        )

    @staticmethod
    def _generar_mensaje_alerta(stock_actual: int, stock_minimo: int, nombre_producto: str) -> Optional[str]:
        if stock_actual > stock_minimo:
            return None

        if stock_actual == 0:
            return f"Producto agotado: '{nombre_producto}' no tiene unidades disponibles."
        return (
            f"Alerta de stock bajo: '{nombre_producto}' tiene {stock_actual} unidad(es), "
            f"por debajo del mínimo configurado ({stock_minimo})."
        )
