import { Router } from 'express';
import { modeloController as c } from '../controllers/modelo.controller.js';

const router = Router();

router.get('/', c.listar);
router.get('/:id', c.obtener);
router.get('/:id/versiones', c.listarVersiones);
router.post('/', c.crear);
router.put('/:id', c.actualizar);
router.delete('/:id', c.eliminar);
router.patch('/:id/restaurar', c.restaurar);

export default router;
