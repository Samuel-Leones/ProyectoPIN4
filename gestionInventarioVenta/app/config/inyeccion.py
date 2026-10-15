from fastapi import Depends
from sqlalchemy.orm import Session

from app.client.cliente_catalogo_motos import ClienteCatalogoMotos, crear_cliente_catalogo_motos
from app.config.base_datos import obtener_sesion
from app.config.seguridad import CodificadorContrasenas, obtener_codificador_contrasenas
from app.repository.categoria_repository import CategoriaRepository
from app.repository.cliente_repository import ClienteRepository
from app.repository.detalle_venta_repository import DetalleVentaRepository
from app.repository.factura_repository import FacturaRepository
from app.repository.modulo_repository import ModuloRepository
from app.repository.modulo_x_rol_repository import ModuloXRolRepository
from app.repository.movimiento_inventario_repository import MovimientoInventarioRepository
from app.repository.producto_compatibilidad_repository import ProductoCompatibilidadRepository
from app.repository.producto_repository import ProductoRepository
from app.repository.proveedor_repository import ProveedorRepository
from app.repository.registro_auditoria_repository import RegistroAuditoriaRepository
from app.repository.rol_repository import RolRepository
from app.repository.usuario_repository import UsuarioRepository
from app.repository.venta_repository import VentaRepository
from app.service.servicio_auditoria import ServicioAuditoria
from app.service.servicio_autenticacion import ServicioAutenticacion
from app.service.servicio_categoria import ServicioCategoria
from app.service.servicio_compatibilidad import ServicioCompatibilidad
from app.service.servicio_cliente import ServicioCliente
from app.service.servicio_factura import ServicioFactura
from app.service.servicio_inventario import ServicioInventario
from app.service.servicio_jwt import ServicioJwt, obtener_servicio_jwt
from app.service.servicio_modulo import ServicioModulo
from app.service.servicio_modulo_x_rol import ServicioModuloXRol
from app.service.servicio_panel import ServicioPanel
from app.service.servicio_producto import ServicioProducto
from app.service.servicio_proveedor import ServicioProveedor
from app.service.servicio_reporte import ServicioReporte
from app.service.servicio_rol import ServicioRol
from app.service.servicio_usuario import ServicioUsuario
from app.service.servicio_venta import ServicioVenta


def obtener_servicio_auditoria(db: Session = Depends(obtener_sesion)) -> ServicioAuditoria:
    return ServicioAuditoria(RegistroAuditoriaRepository(db), UsuarioRepository(db))


def obtener_servicio_autenticacion(
    db: Session = Depends(obtener_sesion),
    codificador: CodificadorContrasenas = Depends(obtener_codificador_contrasenas),
    servicio_jwt: ServicioJwt = Depends(obtener_servicio_jwt),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioAutenticacion:
    return ServicioAutenticacion(
        UsuarioRepository(db),
        RolRepository(db),
        ModuloXRolRepository(db),
        codificador,
        servicio_jwt,
        servicio_auditoria,
    )


def obtener_servicio_categoria(
    db: Session = Depends(obtener_sesion),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioCategoria:
    return ServicioCategoria(CategoriaRepository(db), servicio_auditoria)


def obtener_servicio_proveedor(
    db: Session = Depends(obtener_sesion),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioProveedor:
    return ServicioProveedor(ProveedorRepository(db), servicio_auditoria)


def obtener_servicio_producto(
    db: Session = Depends(obtener_sesion),
    servicio_categoria: ServicioCategoria = Depends(obtener_servicio_categoria),
    servicio_proveedor: ServicioProveedor = Depends(obtener_servicio_proveedor),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioProducto:
    return ServicioProducto(ProductoRepository(db), servicio_categoria, servicio_proveedor, servicio_auditoria)


def obtener_servicio_cliente(
    db: Session = Depends(obtener_sesion),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioCliente:
    return ServicioCliente(ClienteRepository(db), VentaRepository(db), servicio_auditoria)


def obtener_servicio_inventario(
    db: Session = Depends(obtener_sesion),
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioInventario:
    return ServicioInventario(
        MovimientoInventarioRepository(db), servicio_producto, UsuarioRepository(db), servicio_auditoria
    )


def obtener_servicio_factura(db: Session = Depends(obtener_sesion)) -> ServicioFactura:
    return ServicioFactura(FacturaRepository(db))


def obtener_servicio_venta(
    db: Session = Depends(obtener_sesion),
    servicio_cliente: ServicioCliente = Depends(obtener_servicio_cliente),
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
    servicio_inventario: ServicioInventario = Depends(obtener_servicio_inventario),
    servicio_factura: ServicioFactura = Depends(obtener_servicio_factura),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioVenta:
    return ServicioVenta(
        VentaRepository(db),
        servicio_cliente,
        servicio_producto,
        UsuarioRepository(db),
        servicio_inventario,
        servicio_factura,
        servicio_auditoria,
    )


def obtener_servicio_panel(db: Session = Depends(obtener_sesion)) -> ServicioPanel:
    return ServicioPanel(VentaRepository(db), ProductoRepository(db), ClienteRepository(db))


def obtener_servicio_reporte(db: Session = Depends(obtener_sesion)) -> ServicioReporte:
    return ServicioReporte(VentaRepository(db), DetalleVentaRepository(db), ProductoRepository(db))


def obtener_servicio_usuario(
    db: Session = Depends(obtener_sesion),
    codificador: CodificadorContrasenas = Depends(obtener_codificador_contrasenas),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioUsuario:
    return ServicioUsuario(UsuarioRepository(db), RolRepository(db), codificador, servicio_auditoria)


def obtener_servicio_rol(
    db: Session = Depends(obtener_sesion),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioRol:
    return ServicioRol(RolRepository(db), UsuarioRepository(db), servicio_auditoria)


def obtener_servicio_modulo(
    db: Session = Depends(obtener_sesion),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioModulo:
    return ServicioModulo(ModuloRepository(db), servicio_auditoria)


def obtener_servicio_modulo_x_rol(
    db: Session = Depends(obtener_sesion),
    servicio_rol: ServicioRol = Depends(obtener_servicio_rol),
    servicio_modulo: ServicioModulo = Depends(obtener_servicio_modulo),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioModuloXRol:
    return ServicioModuloXRol(ModuloXRolRepository(db), servicio_rol, servicio_modulo, servicio_auditoria)


def obtener_cliente_catalogo_motos() -> ClienteCatalogoMotos:
    return crear_cliente_catalogo_motos()


def obtener_servicio_compatibilidad(
    db: Session = Depends(obtener_sesion),
    servicio_producto: ServicioProducto = Depends(obtener_servicio_producto),
    cliente_catalogo: ClienteCatalogoMotos = Depends(obtener_cliente_catalogo_motos),
    servicio_auditoria: ServicioAuditoria = Depends(obtener_servicio_auditoria),
) -> ServicioCompatibilidad:
    return ServicioCompatibilidad(
        ProductoCompatibilidadRepository(db), servicio_producto, cliente_catalogo, servicio_auditoria
    )
