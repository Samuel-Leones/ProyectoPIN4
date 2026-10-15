import { readFile } from 'node:fs/promises';
import { consultar, ejecutar } from './database.js';
import { CATALOGO_INICIAL } from './datos_iniciales.js';

const RUTA_ESQUEMA = new URL('../../database/esquema_mysql.sql', import.meta.url);

async function crearTablas() {
  const sql = await readFile(RUTA_ESQUEMA, 'utf8');
  const sentencias = sql
    .split('\n')
    .filter((linea) => !linea.trim().startsWith('--'))
    .join('\n')
    .split(';')
    .map((s) => s.trim())
    .filter(Boolean);
  for (const sentencia of sentencias) {
    await ejecutar(sentencia);
  }
}

async function cargarDatosDeEjemplo() {
  const [{ total }] = await consultar('SELECT COUNT(*) AS total FROM marcas');
  if (Number(total) > 0) return;

  for (const { marca, pais, modelos } of CATALOGO_INICIAL) {
    const { insertId: marcaId } = await ejecutar('INSERT INTO marcas (nombre, pais_origen) VALUES (?, ?)', [marca, pais]);
    for (const { nombre, tipo, versiones } of modelos) {
      const { insertId: modeloId } = await ejecutar(
        'INSERT INTO modelos (marca_id, nombre, tipo) VALUES (?, ?, ?)',
        [marcaId, nombre, tipo],
      );
      for (const [anio, cilindraje] of versiones) {
        await ejecutar('INSERT INTO versiones (modelo_id, anio, cilindraje) VALUES (?, ?, ?)', [modeloId, anio, cilindraje]);
      }
    }
  }
}

export async function inicializarBaseDatos() {
  await crearTablas();
  await cargarDatosDeEjemplo();
}
