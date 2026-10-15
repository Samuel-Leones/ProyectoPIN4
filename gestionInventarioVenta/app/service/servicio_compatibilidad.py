from app.client.cliente_catalogo_motos import ClienteCatalogoMotos
from app.dto.base import campos_auditoria
from app.dto.compatibilidad.compatibilidad_request import CompatibilidadRequest
from app.dto.compatibilidad.compatibilidad_response import CompatibilidadResponse
from app.exception.api_exception import RecursoDuplicadoException, RecursoNoEncontradoException
from app.model.accion_auditoria import AccionAuditoria
from app.model.producto_compatibilidad import ProductoCompatibilidad
from app.repository.producto_compatibilidad_repository import ProductoCompatibilidadRepository
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_producto import ServicioProducto


class ServicioCompatibilidad:

    def __init__(
        self,
        compatibilidad_repository: ProductoCompatibilidadRepository,
        servicio_producto: ServicioProducto,
        cliente_catalogo: ClienteCatalogoMotos,
        servicio_auditoria: ServicioAuditoria,
    ):
        self.compatibilidad_repository = compatibilidad_repository
        self.servicio_producto = servicio_producto
        self.cliente_catalogo = cliente_catalogo
        self.servicio_auditoria = servicio_auditoria

    def agregar(self, producto_id: int, request: CompatibilidadRequest, responsable: str) -> CompatibilidadResponse:
        producto = self.servicio_producto.obtener_entidad_activa_o_lanzar(producto_id)

        existente = self.compatibilidad_repository.find_by_producto_id_and_version_moto_id(
            producto.id, request.version_moto_id
        )
        if existente is not None and existente.estado:
            raise RecursoDuplicadoException("El producto ya es compatible con esa moto")

        version = self.cliente_catalogo.obtener_version(request.version_moto_id)

        if existente is None:
            compatibilidad = ProductoCompatibilidad(
                producto_id=producto.id,
                version_moto_id=version.id,
                descripcion_moto=version.descripcion,
            )
            accion = AccionAuditoria.CREACION
        else:
            compatibilidad = existente
            compatibilidad.estado = True
            compatibilidad.descripcion_moto = version.descripcion
            accion = AccionAuditoria.ACTUALIZACION

        guardada = self.compatibilidad_repository.save(compatibilidad)
        self.servicio_auditoria.registrar(responsable, accion, "ProductoCompatibilidad", guardada.id)
        return self._a_response(guardada)

    def listar(self, producto_id: int) -> list[CompatibilidadResponse]:
        producto = self.servicio_producto.obtener_entidad_activa_o_lanzar(producto_id)
        return [
            self._a_response(c)
            for c in self.compatibilidad_repository.find_all_by_producto_id_and_estado_true(producto.id)
        ]

    def quitar(self, producto_id: int, compatibilidad_id: int, responsable: str) -> None:
        producto = self.servicio_producto.obtener_entidad_activa_o_lanzar(producto_id)

        compatibilidad = self.compatibilidad_repository.find_by_id(compatibilidad_id)
        if compatibilidad is None or not compatibilidad.estado or compatibilidad.producto_id != producto.id:
            raise RecursoNoEncontradoException("Compatibilidad no encontrada")

        compatibilidad.estado = False  # borrado lógico
        self.compatibilidad_repository.save(compatibilidad)
        self.servicio_auditoria.registrar(responsable, AccionAuditoria.ELIMINACION, "ProductoCompatibilidad", compatibilidad_id)

    @staticmethod
    def _a_response(compatibilidad: ProductoCompatibilidad) -> CompatibilidadResponse:
        return CompatibilidadResponse(
            id=compatibilidad.id,
            producto_id=compatibilidad.producto_id,
            version_moto_id=compatibilidad.version_moto_id,
            descripcion_moto=compatibilidad.descripcion_moto,
            **campos_auditoria(compatibilidad),
        )
