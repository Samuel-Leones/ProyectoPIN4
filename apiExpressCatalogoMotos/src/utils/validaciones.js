import { solicitudInvalida } from './errores.js';

export class Validador {
  constructor(body) {
    if (body !== undefined && (body === null || typeof body !== 'object' || Array.isArray(body))) {
      throw solicitudInvalida('Cuerpo de la solicitud inválido o incompleto');
    }
    this.body = body ?? {};
    this.errores = [];
  }

  texto(campo, { requerido = false, max = 255 } = {}) {
    const valor = this.body[campo];
    if (valor === undefined || valor === null) {
      if (requerido) this.errores.push(`${campo}: no debe estar vacío`);
      return null;
    }
    if (typeof valor !== 'string') {
      this.errores.push(`${campo}: debe ser texto`);
      return null;
    }
    const limpio = valor.trim();
    if (limpio === '') {
      if (requerido) this.errores.push(`${campo}: no debe estar vacío`);
      return null;
    }
    if (limpio.length > max) {
      this.errores.push(`${campo}: no debe superar ${max} caracteres`);
      return null;
    }
    return limpio;
  }

  entero(campo, { requerido = true, min, max } = {}) {
    const valor = this.body[campo];
    if (valor === undefined || valor === null || valor === '') {
      if (requerido) this.errores.push(`${campo}: es obligatorio`);
      return null;
    }
    const numero = typeof valor === 'string' && /^-?\d+$/.test(valor.trim()) ? Number(valor) : valor;
    if (!Number.isInteger(numero)) {
      this.errores.push(`${campo}: debe ser un número entero`);
      return null;
    }
    if (min !== undefined && numero < min) {
      this.errores.push(`${campo}: debe ser mayor o igual a ${min}`);
      return null;
    }
    if (max !== undefined && numero > max) {
      this.errores.push(`${campo}: debe ser menor o igual a ${max}`);
      return null;
    }
    return numero;
  }

  validar() {
    if (this.errores.length > 0) throw solicitudInvalida(this.errores.join('; '));
  }
}

/** Convierte un parámetro de la URL (/marcas/5) en número entero positivo. */
export function leerId(valor, nombre = 'id') {
  if (typeof valor !== 'string' || !/^\d+$/.test(valor) || Number(valor) < 1) {
    throw solicitudInvalida(`${nombre}: debe ser un número entero positivo`);
  }
  return Number(valor);
}

export function leerIdOpcional(valor, nombre) {
  if (valor === undefined || valor === '') return undefined;
  return leerId(String(valor), nombre);
}

export function leerTextoOpcional(valor) {
  if (typeof valor !== 'string') return undefined;
  const limpio = valor.trim();
  return limpio === '' ? undefined : limpio;
}
