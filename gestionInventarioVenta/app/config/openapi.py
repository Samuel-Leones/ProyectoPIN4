from fastapi.security import HTTPBearer

NOMBRE_ESQUEMA_BEARER = "bearerAuth"

INFO_OPENAPI = {
    "title": "API — Sistema de Gestión de Inventario y Ventas",
    "version": "1.0.0",
    "description": "API REST para la gestión de inventario, ventas, clientes y reportes de una tienda de accesorios de moto",
}

esquema_bearer = HTTPBearer(
    scheme_name=NOMBRE_ESQUEMA_BEARER,
    bearerFormat="JWT",
    auto_error=False,
)
