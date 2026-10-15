import { formatearFechaHora } from '../utils/fechas.js';

const auditoria = (fila) => ({
  estado: Boolean(fila.estado),
  creado: formatearFechaHora(fila.creado),
  actualizado: formatearFechaHora(fila.actualizado),
});

export const aMarcaRespuesta = (fila) => ({
  id: Number(fila.id),
  nombre: fila.nombre,
  paisOrigen: fila.pais_origen,
  ...auditoria(fila),
});

export const aModeloRespuesta = (fila) => ({
  id: Number(fila.id),
  marcaId: Number(fila.marca_id),
  nombreMarca: fila.marca_nombre,
  nombre: fila.nombre,
  tipo: fila.tipo,
  ...auditoria(fila),
});

export const aVersionRespuesta = (fila) => ({
  id: Number(fila.id),
  modeloId: Number(fila.modelo_id),
  nombreModelo: fila.modelo_nombre,
  marcaId: Number(fila.marca_id),
  nombreMarca: fila.marca_nombre,
  anio: fila.anio,
  cilindraje: fila.cilindraje,
  descripcion: `${fila.marca_nombre} ${fila.modelo_nombre} ${fila.anio}`,
  ...auditoria(fila),
});
