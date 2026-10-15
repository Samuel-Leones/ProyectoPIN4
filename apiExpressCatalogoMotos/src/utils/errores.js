export class ApiError extends Error {
  constructor(status, mensaje) {
    super(mensaje);
    this.status = status;
  }
}

export const solicitudInvalida = (mensaje) => new ApiError(400, mensaje);
export const noAutorizado = (mensaje) => new ApiError(401, mensaje);
export const noEncontrado = (mensaje) => new ApiError(404, mensaje);
export const conflicto = (mensaje) => new ApiError(409, mensaje);
