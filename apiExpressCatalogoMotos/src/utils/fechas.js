import { env } from '../config/env.js';

export function formatearFechaHora(fecha) {
  if (!fecha) return null;
  const f = new Intl.DateTimeFormat('en-CA', {
    timeZone: env.zonaHoraria,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hourCycle: 'h23',
    timeZoneName: 'longOffset',
  }).formatToParts(fecha).reduce((acc, p) => ({ ...acc, [p.type]: p.value }), {});

  const desfase = f.timeZoneName === 'GMT' ? '+00:00' : f.timeZoneName.replace('GMT', '');
  return `${f.year}-${f.month}-${f.day}T${f.hour}:${f.minute}:${f.second}${desfase}`;
}
