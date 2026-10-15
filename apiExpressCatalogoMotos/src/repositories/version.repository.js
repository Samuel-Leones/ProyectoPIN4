import { consultar, ejecutar } from '../config/database.js';

const SELECT_VERSION = `
  SELECT v.id, v.modelo_id, mo.nombre AS modelo_nombre, mo.estado AS modelo_estado,
         ma.id AS marca_id, ma.nombre AS marca_nombre,
         v.anio, v.cilindraje, v.estado, v.creado, v.actualizado
  FROM versiones v
  JOIN modelos mo ON mo.id = v.modelo_id
  JOIN marcas ma ON ma.id = mo.marca_id`;

export const versionRepository = {
  async listarActivas({ modeloId, marcaId, anio } = {}) {
    const condiciones = ['v.estado = 1', 'mo.estado = 1', 'ma.estado = 1'];
    const params = [];
    if (modeloId !== undefined) {
      condiciones.push('v.modelo_id = ?');
      params.push(modeloId);
    }
    if (marcaId !== undefined) {
      condiciones.push('ma.id = ?');
      params.push(marcaId);
    }
    if (anio !== undefined) {
      condiciones.push('v.anio = ?');
      params.push(anio);
    }
    return consultar(
      `${SELECT_VERSION} WHERE ${condiciones.join(' AND ')} ORDER BY ma.nombre, mo.nombre, v.anio, v.cilindraje`,
      params,
    );
  },

  async buscarPorId(id) {
    const filas = await consultar(`${SELECT_VERSION} WHERE v.id = ?`, [id]);
    return filas[0] ?? null;
  },

  async buscarPorModeloAnioCilindraje(modeloId, anio, cilindraje) {
    const filas = await consultar(
      `${SELECT_VERSION} WHERE v.modelo_id = ? AND v.anio = ? AND v.cilindraje = ?`,
      [modeloId, anio, cilindraje],
    );
    return filas[0] ?? null;
  },

  async crear({ modeloId, anio, cilindraje }) {
    const { insertId } = await ejecutar('INSERT INTO versiones (modelo_id, anio, cilindraje) VALUES (?, ?, ?)', [modeloId, anio, cilindraje]);
    return insertId;
  },

  async actualizar(id, { modeloId, anio, cilindraje }) {
    await ejecutar('UPDATE versiones SET modelo_id = ?, anio = ?, cilindraje = ? WHERE id = ?', [modeloId, anio, cilindraje, id]);
  },

  async cambiarEstado(id, estado) {
    await ejecutar('UPDATE versiones SET estado = ? WHERE id = ?', [estado ? 1 : 0, id]);
  },
};
