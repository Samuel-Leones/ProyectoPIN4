import { env } from '../config/env.js';
import { noAutorizado } from '../utils/errores.js';

const METODOS_DE_LECTURA = new Set(['GET', 'HEAD', 'OPTIONS']);

export function exigirApiKey(req, _res, next) {
  if (!env.apiKey || METODOS_DE_LECTURA.has(req.method)) return next();
  if (req.get('x-api-key') !== env.apiKey) {
    return next(noAutorizado('API key inválida o ausente (encabezado x-api-key)'));
  }
  return next();
}
