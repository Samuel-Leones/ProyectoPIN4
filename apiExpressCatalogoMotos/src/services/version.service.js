import { modeloRepository } from '../repositories/modelo.repository.js';
import { versionRepository } from '../repositories/version.repository.js';
import { conflicto, noEncontrado } from '../utils/errores.js';
import { Validador } from '../utils/validaciones.js';
import { aVersionRespuesta } from './mapeadores.js';

async function buscarActivaOLanzar(id) {
  const version = await versionRepository.buscarPorId(id);
  if (!version || !version.estado || !version.modelo_estado) throw noEncontrado('Versión no encontrada');
  return version;
}

function leerDatos(body) {
  const v = new Validador(body);
  const datos = {
    modeloId: v.entero('modeloId', { min: 1 }),
    anio: v.entero('anio', { min: 1950, max: new Date().getFullYear() + 1 }),
    cilindraje: v.entero('cilindraje', { min: 1, max: 3000 }),
  };
  v.validar();
  return datos;
}

async function validarModeloActivo(modeloId) {
  const modelo = await modeloRepository.buscarPorId(modeloId);
  if (!modelo || !modelo.estado || !modelo.marca_estado) throw noEncontrado('Modelo no encontrado');
}

async function validarCombinacionLibre({ modeloId, anio, cilindraje }, idActual) {
  const existente = await versionRepository.buscarPorModeloAnioCilindraje(modeloId, anio, cilindraje);
  if (existente && Number(existente.id) !== idActual) {
    throw conflicto(
      existente.estado
        ? 'Ya existe una versión con ese modelo, año y cilindraje'
        : `Ya existe una versión con ese modelo, año y cilindraje pero está inactiva; restáurala con PATCH /versiones/${existente.id}/restaurar`,
    );
  }
}

export const versionService = {
  async listar(filtros) {
    return (await versionRepository.listarActivas(filtros)).map(aVersionRespuesta);
  },

  async obtener(id) {
    return aVersionRespuesta(await buscarActivaOLanzar(id));
  },

  async crear(body) {
    const datos = leerDatos(body);
    await validarModeloActivo(datos.modeloId);
    await validarCombinacionLibre(datos);
    const id = await versionRepository.crear(datos);
    return aVersionRespuesta(await versionRepository.buscarPorId(id));
  },

  async actualizar(id, body) {
    await buscarActivaOLanzar(id);
    const datos = leerDatos(body);
    await validarModeloActivo(datos.modeloId);
    await validarCombinacionLibre(datos, id);
    await versionRepository.actualizar(id, datos);
    return aVersionRespuesta(await versionRepository.buscarPorId(id));
  },

  async eliminar(id) {
    await buscarActivaOLanzar(id);
    await versionRepository.cambiarEstado(id, false);
  },

  async restaurar(id) {
    const version = await versionRepository.buscarPorId(id);
    if (!version) throw noEncontrado('Versión no encontrada');
    if (version.estado) throw conflicto('La versión ya está activa');
    if (!version.modelo_estado) {
      throw conflicto(`El modelo de esta versión está inactivo; restáuralo primero con PATCH /modelos/${version.modelo_id}/restaurar`);
    }
    await versionRepository.cambiarEstado(id, true);
    return aVersionRespuesta(await versionRepository.buscarPorId(id));
  },
};
