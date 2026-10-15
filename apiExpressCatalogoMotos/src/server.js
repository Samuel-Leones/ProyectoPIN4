import { crearApp } from './app.js';
import { cerrarBaseDatos, conectarBaseDatos } from './config/database.js';
import { env } from './config/env.js';
import { inicializarBaseDatos } from './config/inicializador.js';

function explicarErrorDeBaseDatos(error) {
  switch (error.code) {
    case 'ECONNREFUSED':
      return `No se pudo conectar con MySQL (${env.db.host}:${env.db.puerto}). ¿Está encendido? En XAMPP, pulsa "Start" en MySQL.`;
    case 'ER_ACCESS_DENIED_ERROR':
      return 'MySQL rechazó el usuario o la contraseña. Revisa DB_USER y DB_PASSWORD en el archivo .env.';
    case 'ER_BAD_DB_ERROR':
      return `La base de datos "${env.db.nombre}" no existe y no se pudo crear. Revisa DB_NAME y los permisos del usuario.`;
    default:
      return error.message;
  }
}

async function iniciar() {
  try {
    await conectarBaseDatos();
    await inicializarBaseDatos();
  } catch (error) {
    console.error(`\nNo se pudo iniciar la API: ${explicarErrorDeBaseDatos(error)}\n`);
    process.exit(1);
  }

  const servidor = crearApp().listen(env.puerto, () => {
    console.log(`API de catálogo de motos lista en http://localhost:${env.puerto}`);
    console.log(`Documentación (Swagger):       http://localhost:${env.puerto}/docs`);
  });

  const apagar = async () => {
    servidor.close();
    await cerrarBaseDatos();
    process.exit(0);
  };
  process.on('SIGINT', apagar);
  process.on('SIGTERM', apagar);
}

iniciar();
