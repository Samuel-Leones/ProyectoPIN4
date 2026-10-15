from app.dto.base import campos_auditoria
from app.dto.factura.factura_response import FacturaResponse
from app.exception.api_exception import RecursoNoEncontradoException
from app.model.factura import Factura
from app.model.venta import Venta
from app.repository.factura_repository import FacturaRepository
from app.service.mapeador_venta import a_venta_response
from app.util.generador_numero_factura import GeneradorNumeroFactura


class ServicioFactura:
    def __init__(self, factura_repository: FacturaRepository):
        self.factura_repository = factura_repository

    def generar_para_venta(self, venta: Venta) -> Factura:
        secuencia = self.factura_repository.count() + 1
        numero_factura = GeneradorNumeroFactura.generar(secuencia)

        while self.factura_repository.exists_by_numero_factura(numero_factura):
            secuencia += 1
            numero_factura = GeneradorNumeroFactura.generar(secuencia)

        factura = Factura(venta=venta, numero_factura=numero_factura)
        return self.factura_repository.save(factura)

    def obtener_por_venta_id(self, venta_id: int) -> FacturaResponse:
        factura = self.factura_repository.find_by_venta_id(venta_id)
        if factura is None:
            raise RecursoNoEncontradoException("La venta aún no tiene una factura generada")
        return self._a_response(factura)

    @staticmethod
    def _a_response(factura: Factura) -> FacturaResponse:
        return FacturaResponse(
            id=factura.id,
            numero_factura=factura.numero_factura,
            venta=a_venta_response(factura.venta),
            **campos_auditoria(factura),
        )
