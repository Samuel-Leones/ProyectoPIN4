import { modeloService } from '../services/modelo.service.js';
import { leerId, leerIdOpcional, leerTextoOpcional } from '../utils/validaciones.js';

export const modeloController = {
  listar: async (req, res) =>
    res.json(
      await modeloService.listar({
        marcaId: leerIdOpcional(req.query.marcaId, 'marcaId'),
        nombre: leerTextoOpcional(req.query.nombre),
      }),
    ),
  obtener: async (req, res) => res.json(await modeloService.obtener(leerId(req.params.id))),
  listarVersiones: async (req, res) => res.json(await modeloService.listarVersiones(leerId(req.params.id))),
  crear: async (req, res) => res.status(201).json(await modeloService.crear(req.body)),
  actualizar: async (req, res) => res.json(await modeloService.actualizar(leerId(req.params.id), req.body)),
  eliminar: async (req, res) => {
    await modeloService.eliminar(leerId(req.params.id));
    res.status(204).end();
  },
  restaurar: async (req, res) => res.json(await modeloService.restaurar(leerId(req.params.id))),
};
