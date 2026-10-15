import dotenv from 'dotenv';

dotenv.config({ quiet: true });

const entero = (nombre, porDefecto) => Number.parseInt(process.env[nombre] ?? String(porDefecto), 10);
const texto = (nombre, porDefecto = '') => (process.env[nombre] ?? porDefecto).trim();

export const env = {
  puerto: entero('PORT', 4000),
  zonaHoraria: texto('ZONA_HORARIA', 'America/Bogota'),
  apiKey: texto('API_KEY'),
  corsOrigenes: texto('CORS_ORIGENES')
    .split(',')
    .map((o) => o.trim())
    .filter(Boolean),
  db: {
    url: texto('DATABASE_URL'),
    host: texto('DB_HOST', 'localhost'),
    puerto: entero('DB_PORT', 3306),
    usuario: texto('DB_USER', 'root'),
    contrasena: process.env.DB_PASSWORD ?? '',
    nombre: texto('DB_NAME', 'catalogo_motos'),
    ssl: texto('DB_SSL', 'false').toLowerCase() === 'true',
  },
};
