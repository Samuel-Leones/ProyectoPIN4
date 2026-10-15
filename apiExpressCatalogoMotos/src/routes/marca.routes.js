import { Router } from 'express';
import { marcaController as c } from '../controllers/marca.controller.js';

const router = Router();

router.get('/', c.listar);
router.get('/:id', c.obtener);
router.get('/:id/modelos', c.listarModelos);
router.post('/', c.crear);
router.put('/:id', c.actualizar);
router.delete('/:id', c.eliminar);
router.patch('/:id/restaurar', c.restaurar);

export default router;
