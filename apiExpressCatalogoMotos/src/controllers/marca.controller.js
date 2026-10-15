import { marcaService } from '../services/marca.service.js';
import { leerId, leerTextoOpcional } from '../utils/validaciones.js';

export const marcaController = {
  listar: async (req, res) => res.json(await marcaService.listar(leerTextoOpcional(req.query.nombre))),
  obtener: async (req, res) => res.json(await marcaService.obtener(leerId(req.params.id))),
  listarModelos: async (req, res) => res.json(await marcaService.listarModelos(leerId(req.params.id))),
  crear: async (req, res) => res.status(201).json(await marcaService.crear(req.body)),
  actualizar: async (req, res) => res.json(await marcaService.actualizar(leerId(req.params.id), req.body)),
  eliminar: async (req, res) => {
    await marcaService.eliminar(leerId(req.params.id));
    res.status(204).end();
  },
  restaurar: async (req, res) => res.json(await marcaService.restaurar(leerId(req.params.id))),
};
