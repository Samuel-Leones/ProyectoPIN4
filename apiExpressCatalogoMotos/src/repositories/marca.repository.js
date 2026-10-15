import { consultar, ejecutar } from '../config/database.js';

export const marcaRepository = {
  async listarActivas(nombre) {
    if (nombre) {
      return consultar('SELECT * FROM marcas WHERE estado = 1 AND nombre LIKE ? ORDER BY nombre', [`%${nombre}%`]);
    }
    return consultar('SELECT * FROM marcas WHERE estado = 1 ORDER BY nombre');
  },

  async buscarPorId(id) {
    const filas = await consultar('SELECT * FROM marcas WHERE id = ?', [id]);
    return filas[0] ?? null;
  },

  async buscarPorNombre(nombre) {
    const filas = await consultar('SELECT * FROM marcas WHERE nombre = ?', [nombre]);
    return filas[0] ?? null;
  },

  async crear({ nombre, paisOrigen }) {
    const { insertId } = await ejecutar('INSERT INTO marcas (nombre, pais_origen) VALUES (?, ?)', [nombre, paisOrigen]);
    return insertId;
  },

  async actualizar(id, { nombre, paisOrigen }) {
    await ejecutar('UPDATE marcas SET nombre = ?, pais_origen = ? WHERE id = ?', [nombre, paisOrigen, id]);
  },

  async cambiarEstado(id, estado) {
    await ejecutar('UPDATE marcas SET estado = ? WHERE id = ?', [estado ? 1 : 0, id]);
  },

  async contarModelosActivos(marcaId) {
    const [{ total }] = await consultar('SELECT COUNT(*) AS total FROM modelos WHERE marca_id = ? AND estado = 1', [marcaId]);
    return Number(total);
  },
};
