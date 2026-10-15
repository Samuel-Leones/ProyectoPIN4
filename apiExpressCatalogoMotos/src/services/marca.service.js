// Capa service: aquí viven las reglas de negocio.
import { marcaRepository } from '../repositories/marca.repository.js';
import { modeloRepository } from '../repositories/modelo.repository.js';
import { conflicto, noEncontrado } from '../utils/errores.js';
import { Validador } from '../utils/validaciones.js';
import { aMarcaRespuesta, aModeloRespuesta } from './mapeadores.js';

async function buscarActivaOLanzar(id) {
  const marca = await marcaRepository.buscarPorId(id);
  if (!marca || !marca.estado) throw noEncontrado('Marca no encontrada');
  return marca;
}

function leerDatos(body) {
  const v = new Validador(body);
  const datos = {
    nombre: v.texto('nombre', { requerido: true, max: 100 }),
    paisOrigen: v.texto('paisOrigen', { max: 100 }),
  };
  v.validar();
  return datos;
}

/** El nombre es único en toda la tabla (incluidas las eliminadas), por eso se avisa si está inactiva. */
async function validarNombreLibre(nombre, idActual) {
  const existente = await marcaRepository.buscarPorNombre(nombre);
  if (existente && Number(existente.id) !== idActual) {
    throw conflicto(
      existente.estado
        ? 'Ya existe una marca con ese nombre'
        : `Ya existe una marca con ese nombre pero está inactiva; restáurala con PATCH /marcas/${existente.id}/restaurar`,
    );
  }
}

export const marcaService = {
  async listar(nombre) {
    return (await marcaRepository.listarActivas(nombre)).map(aMarcaRespuesta);
  },

  async obtener(id) {
    return aMarcaRespuesta(await buscarActivaOLanzar(id));
  },

  async listarModelos(id) {
    await buscarActivaOLanzar(id);
    return (await modeloRepository.listarActivos({ marcaId: id })).map(aModeloRespuesta);
  },

  async crear(body) {
    const datos = leerDatos(body);
    await validarNombreLibre(datos.nombre);
    const id = await marcaRepository.crear(datos);
    return aMarcaRespuesta(await marcaRepository.buscarPorId(id));
  },

  async actualizar(id, body) {
    await buscarActivaOLanzar(id);
    const datos = leerDatos(body);
    await validarNombreLibre(datos.nombre, id);
    await marcaRepository.actualizar(id, datos);
    return aMarcaRespuesta(await marcaRepository.buscarPorId(id));
  },

  /** Borrado lógico: la fila no se borra, solo pasa a estado = 0. */
  async eliminar(id) {
    await buscarActivaOLanzar(id);
    if ((await marcaRepository.contarModelosActivos(id)) > 0) {
      throw conflicto('No se puede eliminar la marca porque tiene modelos activos.');
    }
    await marcaRepository.cambiarEstado(id, false);
  },

  async restaurar(id) {
    const marca = await marcaRepository.buscarPorId(id);
    if (!marca) throw noEncontrado('Marca no encontrada');
    if (marca.estado) throw conflicto('La marca ya está activa');
    await marcaRepository.cambiarEstado(id, true);
    return aMarcaRespuesta(await marcaRepository.buscarPorId(id));
  },
};
