import { STATUS_CODES } from 'node:http';
import { ApiError, noEncontrado } from '../utils/errores.js';
import { formatearFechaHora } from '../utils/fechas.js';

export function rutaNoEncontrada(req, _res, next) {
  next(noEncontrado('Not Found'));
}

function traducir(error) {
  if (error instanceof ApiError) return { status: error.status, mensaje: error.message };

  if (error.type === 'entity.parse.failed') {
    return { status: 400, mensaje: 'Cuerpo de la solicitud inválido o incompleto' };
  }
  if (error.type === 'entity.too.large') return { status: 413, mensaje: 'Cuerpo de la solicitud demasiado grande' };

  switch (error.code) {
    case 'ER_DUP_ENTRY':
      return { status: 409, mensaje: 'Ya existe un registro con esos datos' };
    case 'ER_NO_REFERENCED_ROW_2':
      return { status: 404, mensaje: 'El registro relacionado no existe' };
    case 'ER_ROW_IS_REFERENCED_2':
      return { status: 409, mensaje: 'No se puede eliminar: otros registros dependen de este' };
    default:
      return null;
  }
}

export function manejadorErrores(error, req, res, _next) {
  const conocido = traducir(error);
  if (!conocido) console.error(`Error inesperado en ${req.method} ${req.originalUrl}:`, error);

  const status = conocido?.status ?? 500;
  res.status(status).json({
    timestamp: formatearFechaHora(new Date()),
    status,
    error: STATUS_CODES[status],
    message: conocido?.mensaje ?? 'Error interno del servidor',
    path: req.originalUrl.split('?')[0],
  });
}
