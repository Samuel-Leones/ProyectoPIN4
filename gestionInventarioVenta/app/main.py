from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI

from app.config.base_datos import SesionLocal, inicializar_esquema
from app.config.configuracion import configuracion
from app.config.inicializador_datos import ejecutar_inicializador
from app.config.openapi import INFO_OPENAPI
from app.config.seguridad import autorizar_solicitud, configurar_cors
from app.controller import (
    controlador_auditoria,
    controlador_autenticacion,
    controlador_categoria,
    controlador_cliente,
    controlador_inventario,
    controlador_modulo,
    controlador_modulo_x_rol,
    controlador_panel,
    controlador_producto,
    controlador_proveedor,
    controlador_reporte,
    controlador_rol,
    controlador_usuario,
    controlador_venta,
)
from app.exception.global_exception_handler import registrar_manejadores


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    inicializar_esquema()
    with SesionLocal() as sesion:
        ejecutar_inicializador(sesion)
    yield


app = FastAPI(
    **INFO_OPENAPI,
    docs_url="/swagger-ui.html",
    openapi_url="/v3/api-docs",
    redoc_url=None,
    lifespan=ciclo_de_vida,
    dependencies=[Depends(autorizar_solicitud)],  
)

registrar_manejadores(app)
configurar_cors(app) 

app.include_router(controlador_autenticacion.router)
app.include_router(controlador_auditoria.router)
app.include_router(controlador_categoria.router)
app.include_router(controlador_cliente.router)
app.include_router(controlador_inventario.router)
app.include_router(controlador_modulo.router)
app.include_router(controlador_modulo_x_rol.router)
app.include_router(controlador_panel.router)
app.include_router(controlador_producto.router)
app.include_router(controlador_proveedor.router)
app.include_router(controlador_reporte.router)
app.include_router(controlador_rol.router)
app.include_router(controlador_usuario.router)
app.include_router(controlador_venta.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=configuracion.puerto_servidor, reload=True)
