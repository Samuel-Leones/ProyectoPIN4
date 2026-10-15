import { versionService } from '../services/version.service.js';
import { leerId, leerIdOpcional } from '../utils/validaciones.js';

export const versionController = {
  listar: async (req, res) =>
    res.json(
      await versionService.listar({
        marcaId: leerIdOpcional(req.query.marcaId, 'marcaId'),
        modeloId: leerIdOpcional(req.query.modeloId, 'modeloId'),
        anio: leerIdOpcional(req.query.anio, 'anio'),
      }),
    ),
  obtener: async (req, res) => res.json(await versionService.obtener(leerId(req.params.id))),
  crear: async (req, res) => res.status(201).json(await versionService.crear(req.body)),
  actualizar: async (req, res) => res.json(await versionService.actualizar(leerId(req.params.id), req.body)),
  eliminar: async (req, res) => {
    await versionService.eliminar(leerId(req.params.id));
    res.status(204).end();
  },
  restaurar: async (req, res) => res.json(await versionService.restaurar(leerId(req.params.id))),
};
