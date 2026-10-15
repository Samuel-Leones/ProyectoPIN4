import { consultar, ejecutar } from '../config/database.js';

const SELECT_MODELO = `
  SELECT mo.id, mo.marca_id, ma.nombre AS marca_nombre, ma.estado AS marca_estado,
         mo.nombre, mo.tipo, mo.estado, mo.creado, mo.actualizado
  FROM modelos mo
  JOIN marcas ma ON ma.id = mo.marca_id`;

export const modeloRepository = {
  async listarActivos({ marcaId, nombre } = {}) {
    const condiciones = ['mo.estado = 1', 'ma.estado = 1'];
    const params = [];
    if (marcaId !== undefined) {
      condiciones.push('mo.marca_id = ?');
      params.push(marcaId);
    }
    if (nombre) {
      condiciones.push('mo.nombre LIKE ?');
      params.push(`%${nombre}%`);
    }
    return consultar(`${SELECT_MODELO} WHERE ${condiciones.join(' AND ')} ORDER BY ma.nombre, mo.nombre`, params);
  },

  async buscarPorId(id) {
    const filas = await consultar(`${SELECT_MODELO} WHERE mo.id = ?`, [id]);
    return filas[0] ?? null;
  },

  async buscarPorMarcaYNombre(marcaId, nombre) {
    const filas = await consultar(`${SELECT_MODELO} WHERE mo.marca_id = ? AND mo.nombre = ?`, [marcaId, nombre]);
    return filas[0] ?? null;
  },

  async crear({ marcaId, nombre, tipo }) {
    const { insertId } = await ejecutar('INSERT INTO modelos (marca_id, nombre, tipo) VALUES (?, ?, ?)', [marcaId, nombre, tipo]);
    return insertId;
  },

  async actualizar(id, { marcaId, nombre, tipo }) {
    await ejecutar('UPDATE modelos SET marca_id = ?, nombre = ?, tipo = ? WHERE id = ?', [marcaId, nombre, tipo, id]);
  },

  async cambiarEstado(id, estado) {
    await ejecutar('UPDATE modelos SET estado = ? WHERE id = ?', [estado ? 1 : 0, id]);
  },

  async contarVersionesActivas(modeloId) {
    const [{ total }] = await consultar('SELECT COUNT(*) AS total FROM versiones WHERE modelo_id = ? AND estado = 1', [modeloId]);
    return Number(total);
  },
};
