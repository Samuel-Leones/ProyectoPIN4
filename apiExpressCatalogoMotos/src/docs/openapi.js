const ref = (nombre) => ({ $ref: `#/components/schemas/${nombre}` });
const json = (schema) => ({ 'application/json': { schema } });
const respuesta = (descripcion, schema) => ({ description: descripcion, ...(schema ? { content: json(schema) } : {}) });
const lista = (nombre) => ({ type: 'array', items: ref(nombre) });
const llave = [{ apiKey: [] }];

const idParametro = { name: 'id', in: 'path', required: true, schema: { type: 'integer', minimum: 1 } };
const filtro = (nombre, tipo, descripcion) => ({ name: nombre, in: 'query', required: false, description: descripcion, schema: { type: tipo } });

const errores = {
  400: respuesta('Datos inválidos', ref('Error')),
  404: respuesta('No encontrado', ref('Error')),
  409: respuesta('Conflicto (duplicado o regla de negocio)', ref('Error')),
};
const solo = (...codigos) => Object.fromEntries(codigos.map((c) => [c, errores[c]]));

function crud({ tag, base, singular, plural, schema, request, filtros = [] }) {
  return {
    [base]: {
      get: {
        tags: [tag],
        summary: `Listar ${plural} activos`,
        parameters: filtros,
        responses: { 200: respuesta('Lista', lista(schema)), ...solo(400) },
      },
      post: {
        tags: [tag],
        summary: `Crear ${singular}`,
        security: llave,
        requestBody: { required: true, content: json(ref(request)) },
        responses: { 201: respuesta('Creado', ref(schema)), ...solo(400, 404, 409) },
      },
    },
    [`${base}/{id}`]: {
      get: {
        tags: [tag],
        summary: `Obtener ${singular} por id`,
        parameters: [idParametro],
        responses: { 200: respuesta('Encontrado', ref(schema)), ...solo(400, 404) },
      },
      put: {
        tags: [tag],
        summary: `Actualizar ${singular}`,
        security: llave,
        parameters: [idParametro],
        requestBody: { required: true, content: json(ref(request)) },
        responses: { 200: respuesta('Actualizado', ref(schema)), ...solo(400, 404, 409) },
      },
      delete: {
        tags: [tag],
        summary: `Eliminar ${singular} (borrado lógico: estado = false)`,
        security: llave,
        parameters: [idParametro],
        responses: { 204: respuesta('Eliminado'), ...solo(400, 404, 409) },
      },
    },
    [`${base}/{id}/restaurar`]: {
      patch: {
        tags: [tag],
        summary: `Restaurar ${singular} eliminado (estado = true)`,
        security: llave,
        parameters: [idParametro],
        responses: { 200: respuesta('Restaurado', ref(schema)), ...solo(400, 404, 409) },
      },
    },
  };
}

const fechas = {
  estado: { type: 'boolean', example: true },
  creado: { type: 'string', example: '2026-10-14T09:30:00-05:00' },
  actualizado: { type: 'string', example: '2026-10-14T09:30:00-05:00' },
};

const paths = {
  ...crud({
    tag: 'Marcas', base: '/marcas', singular: 'marca', plural: 'marcas', schema: 'Marca', request: 'MarcaRequest',
    filtros: [filtro('nombre', 'string', 'Busca marcas cuyo nombre contenga este texto')],
  }),
  ...crud({
    tag: 'Modelos', base: '/modelos', singular: 'modelo', plural: 'modelos', schema: 'Modelo', request: 'ModeloRequest',
    filtros: [filtro('marcaId', 'integer', 'Solo los modelos de esta marca'), filtro('nombre', 'string', 'Busca modelos cuyo nombre contenga este texto')],
  }),
  ...crud({
    tag: 'Versiones', base: '/versiones', singular: 'versión', plural: 'versiones', schema: 'Version', request: 'VersionRequest',
    filtros: [
      filtro('marcaId', 'integer', 'Solo las versiones de esta marca'),
      filtro('modeloId', 'integer', 'Solo las versiones de este modelo'),
      filtro('anio', 'integer', 'Solo las versiones de este año'),
    ],
  }),
};

paths['/marcas/{id}/modelos'] = {
  get: {
    tags: ['Marcas'],
    summary: 'Modelos de una marca (para el desplegable en cascada)',
    parameters: [idParametro],
    responses: { 200: respuesta('Lista', lista('Modelo')), ...solo(400, 404) },
  },
};
paths['/modelos/{id}/versiones'] = {
  get: {
    tags: ['Modelos'],
    summary: 'Versiones de un modelo (para el desplegable en cascada)',
    parameters: [idParametro],
    responses: { 200: respuesta('Lista', lista('Version')), ...solo(400, 404) },
  },
};

export const openapi = {
  openapi: '3.0.3',
  info: {
    title: 'API de catálogo de motos',
    version: '1.0.0',
    description:
      'Servicio auxiliar con marcas, modelos y versiones de motos (Node.js + Express + MySQL). ' +
      'Pensado para ser consumido por otros proyectos, por ejemplo para indicar con qué motos es compatible un producto. ' +
      'Las operaciones que modifican datos solo piden la clave (encabezado x-api-key) si el servidor tiene API_KEY configurada.',
  },
  servers: [{ url: '/' }],
  paths,
  components: {
    securitySchemes: { apiKey: { type: 'apiKey', in: 'header', name: 'x-api-key' } },
    schemas: {
      Marca: {
        type: 'object',
        properties: { id: { type: 'integer', example: 1 }, nombre: { type: 'string', example: 'Yamaha' }, paisOrigen: { type: 'string', nullable: true, example: 'Japón' }, ...fechas },
      },
      MarcaRequest: {
        type: 'object',
        required: ['nombre'],
        properties: { nombre: { type: 'string', maxLength: 100, example: 'Yamaha' }, paisOrigen: { type: 'string', maxLength: 100, example: 'Japón' } },
      },
      Modelo: {
        type: 'object',
        properties: {
          id: { type: 'integer', example: 1 }, marcaId: { type: 'integer', example: 1 }, nombreMarca: { type: 'string', example: 'Yamaha' },
          nombre: { type: 'string', example: 'FZ 150' }, tipo: { type: 'string', nullable: true, example: 'Naked' }, ...fechas,
        },
      },
      ModeloRequest: {
        type: 'object',
        required: ['marcaId', 'nombre'],
        properties: { marcaId: { type: 'integer', example: 1 }, nombre: { type: 'string', maxLength: 100, example: 'FZ 150' }, tipo: { type: 'string', maxLength: 50, example: 'Naked' } },
      },
      Version: {
        type: 'object',
        properties: {
          id: { type: 'integer', example: 2 }, modeloId: { type: 'integer', example: 1 }, nombreModelo: { type: 'string', example: 'FZ 150' },
          marcaId: { type: 'integer', example: 1 }, nombreMarca: { type: 'string', example: 'Yamaha' },
          anio: { type: 'integer', example: 2022 }, cilindraje: { type: 'integer', example: 149 },
          descripcion: { type: 'string', example: 'Yamaha FZ 150 2022' }, ...fechas,
        },
      },
      VersionRequest: {
        type: 'object',
        required: ['modeloId', 'anio', 'cilindraje'],
        properties: { modeloId: { type: 'integer', example: 1 }, anio: { type: 'integer', example: 2022 }, cilindraje: { type: 'integer', example: 149 } },
      },
      Error: {
        type: 'object',
        properties: {
          timestamp: { type: 'string', example: '2026-10-14T09:30:00-05:00' }, status: { type: 'integer', example: 404 },
          error: { type: 'string', example: 'Not Found' }, message: { type: 'string', example: 'Marca no encontrada' }, path: { type: 'string', example: '/marcas/99' },
        },
      },
    },
  },
};
