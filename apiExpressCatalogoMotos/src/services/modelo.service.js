import { marcaRepository } from '../repositories/marca.repository.js';
import { modeloRepository } from '../repositories/modelo.repository.js';
import { versionRepository } from '../repositories/version.repository.js';
import { conflicto, noEncontrado } from '../utils/errores.js';
import { Validador } from '../utils/validaciones.js';
import { aModeloRespuesta, aVersionRespuesta } from './mapeadores.js';

async function buscarActivoOLanzar(id) {
  const modelo = await modeloRepository.buscarPorId(id);
  if (!modelo || !modelo.estado || !modelo.marca_estado) throw noEncontrado('Modelo no encontrado');
  return modelo;
}

function leerDatos(body) {
  const v = new Validador(body);
  const datos = {
    marcaId: v.entero('marcaId', { min: 1 }),
    nombre: v.texto('nombre', { requerido: true, max: 100 }),
    tipo: v.texto('tipo', { max: 50 }),
  };
  v.validar();
  return datos;
}

async function validarMarcaActiva(marcaId) {
  const marca = await marcaRepository.buscarPorId(marcaId);
  if (!marca || !marca.estado) throw noEncontrado('Marca no encontrada');
}

async function validarNombreLibre({ marcaId, nombre }, idActual) {
  const existente = await modeloRepository.buscarPorMarcaYNombre(marcaId, nombre);
  if (existente && Number(existente.id) !== idActual) {
    throw conflicto(
      existente.estado
        ? 'Ya existe un modelo con ese nombre en la marca'
        : `Ya existe un modelo con ese nombre en la marca pero está inactivo; restáuralo con PATCH /modelos/${existente.id}/restaurar`,
    );
  }
}

export const modeloService = {
  async listar({ marcaId, nombre }) {
    return (await modeloRepository.listarActivos({ marcaId, nombre })).map(aModeloRespuesta);
  },

  async obtener(id) {
    return aModeloRespuesta(await buscarActivoOLanzar(id));
  },

  async listarVersiones(id) {
    await buscarActivoOLanzar(id);
    return (await versionRepository.listarActivas({ modeloId: id })).map(aVersionRespuesta);
  },

  async crear(body) {
    const datos = leerDatos(body);
    await validarMarcaActiva(datos.marcaId);
    await validarNombreLibre(datos);
    const id = await modeloRepository.crear(datos);
    return aModeloRespuesta(await modeloRepository.buscarPorId(id));
  },

  async actualizar(id, body) {
    await buscarActivoOLanzar(id);
    const datos = leerDatos(body);
    await validarMarcaActiva(datos.marcaId);
    await validarNombreLibre(datos, id);
    await modeloRepository.actualizar(id, datos);
    return aModeloRespuesta(await modeloRepository.buscarPorId(id));
  },

  async eliminar(id) {
    await buscarActivoOLanzar(id);
    if ((await modeloRepository.contarVersionesActivas(id)) > 0) {
      throw conflicto('No se puede eliminar el modelo porque tiene versiones activas.');
    }
    await modeloRepository.cambiarEstado(id, false);
  },

  async restaurar(id) {
    const modelo = await modeloRepository.buscarPorId(id);
    if (!modelo) throw noEncontrado('Modelo no encontrado');
    if (modelo.estado) throw conflicto('El modelo ya está activo');
    if (!modelo.marca_estado) {
      throw conflicto(`La marca de este modelo está inactiva; restáurala primero con PATCH /marcas/${modelo.marca_id}/restaurar`);
    }
    await modeloRepository.cambiarEstado(id, true);
    return aModeloRespuesta(await modeloRepository.buscarPorId(id));
  },
};
