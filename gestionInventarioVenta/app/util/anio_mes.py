from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.config.configuracion import configuracion


def zona() -> ZoneInfo:
    return ZoneInfo(configuracion.zona_horaria)


@dataclass(frozen=True)
class AnioMes:
    anio: int
    mes: int

    def __post_init__(self) -> None:
        if not 1 <= self.mes <= 12:
            raise ValueError(f"Mes inválido: {self.mes}")
        date(self.anio, self.mes, 1)  

    @staticmethod
    def of(anio: int, mes: int) -> "AnioMes":
        return AnioMes(anio, mes)

    @staticmethod
    def now() -> "AnioMes":
        hoy = datetime.now(zona()).date()
        return AnioMes(hoy.year, hoy.month)

    def at_day(self, dia: int) -> date:
        return date(self.anio, self.mes, dia)

    def plus_months(self, meses: int) -> "AnioMes":
        indice = self.anio * 12 + (self.mes - 1) + meses
        return AnioMes(indice // 12, indice % 12 + 1)

    def __str__(self) -> str:
        return f"{self.anio:04d}-{self.mes:02d}"


def inicio_del_dia(fecha: date) -> datetime:
    return datetime(fecha.year, fecha.month, fecha.day, tzinfo=zona())
