import mysql from 'mysql2/promise';
import { env } from './env.js';

const ssl = env.db.ssl ? { rejectUnauthorized: false } : undefined;

let pool;

function opcionesPool() {
  const comunes = {
    waitForConnections: true,
    connectionLimit: 10,
    charset: 'utf8mb4',
    timezone: 'Z',
    ssl,
  };
  if (env.db.url) return { uri: env.db.url, ...comunes };
  return {
    host: env.db.host,
    port: env.db.puerto,
    user: env.db.usuario,
    password: env.db.contrasena,
    database: env.db.nombre,
    ...comunes,
  };
}

async function crearBaseSiNoExiste() {
  if (env.db.url) return; 
  if (!/^[A-Za-z0-9_]+$/.test(env.db.nombre)) {
    throw new Error('DB_NAME solo puede tener letras, números y guion bajo');
  }
  const conexion = await mysql.createConnection({
    host: env.db.host,
    port: env.db.puerto,
    user: env.db.usuario,
    password: env.db.contrasena,
    ssl,
  });
  try {
    await conexion.query(
      `CREATE DATABASE IF NOT EXISTS \`${env.db.nombre}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`,
    );
  } catch (error) {
    if (!['ER_DBACCESS_DENIED_ERROR', 'ER_SPECIFIC_ACCESS_DENIED_ERROR'].includes(error.code)) throw error;
  } finally {
    await conexion.end();
  }
}

export async function conectarBaseDatos() {
  await crearBaseSiNoExiste();
  pool = mysql.createPool(opcionesPool());
  pool.pool.on('connection', (conexion) => conexion.query("SET time_zone = '+00:00'"));
  await pool.query('SELECT 1');
  return pool;
}

export async function cerrarBaseDatos() {
  if (pool) await pool.end();
}

const sinUndefined = (params) => params.map((p) => (p === undefined ? null : p));

export async function consultar(sql, params = []) {
  const [filas] = await pool.execute(sql, sinUndefined(params));
  return filas;
}

export async function ejecutar(sql, params = []) {
  const [resultado] = await pool.execute(sql, sinUndefined(params));
  return resultado;
}
