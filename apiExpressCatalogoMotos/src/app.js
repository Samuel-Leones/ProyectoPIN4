import cors from 'cors';
import express from 'express';
import swaggerUi from 'swagger-ui-express';
import { consultar } from './config/database.js';
import { env } from './config/env.js';
import { openapi } from './docs/openapi.js';
import { exigirApiKey } from './middlewares/api-key.js';
import { manejadorErrores, rutaNoEncontrada } from './middlewares/error-handler.js';
import marcaRoutes from './routes/marca.routes.js';
import modeloRoutes from './routes/modelo.routes.js';
import versionRoutes from './routes/version.routes.js';

export function crearApp() {
  const app = express();
  app.disable('x-powered-by');

  app.use(
    cors({
      origin: env.corsOrigenes.length > 0 ? env.corsOrigenes : '*',
      methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
      allowedHeaders: ['Content-Type', 'x-api-key'],
    }),
  );
  app.use(express.json());

  app.get('/', (_req, res) =>
    res.json({
      servicio: 'API de catálogo de motos',
      descripcion: 'Marcas, modelos y versiones de motos (servicio auxiliar)',
      documentacion: '/docs',
      endpoints: ['/marcas', '/modelos', '/versiones'],
    }),
  );
  app.get('/salud', async (_req, res) => {
    try {
      await consultar('SELECT 1');
      res.json({ estado: 'ok', baseDatos: 'ok' });
    } catch {
      res.status(503).json({ estado: 'error', baseDatos: 'sin conexión' });
    }
  });
  app.get('/openapi.json', (_req, res) => res.json(openapi));
  app.use('/docs', swaggerUi.serve, swaggerUi.setup(openapi, { customSiteTitle: 'Catálogo de motos - API' }));

  app.use(exigirApiKey);

  app.use('/marcas', marcaRoutes);
  app.use('/modelos', modeloRoutes);
  app.use('/versiones', versionRoutes);

  app.use(rutaNoEncontrada);
  app.use(manejadorErrores);
  return app;
}
