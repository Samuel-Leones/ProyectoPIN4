import { Router } from 'express';
import { versionController as c } from '../controllers/version.controller.js';

const router = Router();

router.get('/', c.listar);
router.get('/:id', c.obtener);
router.post('/', c.crear);
router.put('/:id', c.actualizar);
router.delete('/:id', c.eliminar);
router.patch('/:id/restaurar', c.restaurar);

export default router;
