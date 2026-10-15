import re
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import AfterValidator

_LOCAL = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
_ETIQUETA = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
_PATRON_EMAIL = re.compile(rf"^({_LOCAL})@({_ETIQUETA}(?:\.{_ETIQUETA})*)$")


def _es_email_valido(valor: str) -> bool:
    if valor == "":
        return True  
    coincidencia = _PATRON_EMAIL.match(valor)
    if not coincidencia:
        return False
    return len(coincidencia.group(1)) <= 64 and len(coincidencia.group(2)) <= 255


def _no_blank(valor: str) -> str:
    if valor is None or valor.strip() == "":
        raise ValueError("must not be blank")
    return valor


def _no_blank_y_email(valor: str) -> str:
    _no_blank(valor)
    if not _es_email_valido(valor):
        raise ValueError("must be a well-formed email address")
    return valor


def _email_opcional(valor: Optional[str]) -> Optional[str]:
    if valor is not None and not _es_email_valido(valor):
        raise ValueError("must be a well-formed email address")
    return valor


def _contrasena_valida(valor: str) -> str:
    _no_blank(valor)
    if len(valor) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    return valor


def _contrasena_opcional(valor: Optional[str]) -> Optional[str]:
    if valor is not None and len(valor) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    return valor


def _positivo(valor: int) -> int:
    if valor <= 0:
        raise ValueError("must be greater than 0")
    return valor


def _positivo_o_cero(valor: int) -> int:
    if valor < 0:
        raise ValueError("must be greater than or equal to 0")
    return valor


def _precio_positivo(valor: Decimal) -> Decimal:
    if valor <= 0:
        raise ValueError("El precio debe ser mayor a 0")
    return valor


def _lista_no_vacia_venta(valor: list) -> list:
    if len(valor) == 0:
        raise ValueError("La venta debe incluir al menos un producto")
    return valor


NotBlank = Annotated[str, AfterValidator(_no_blank)]                      
NotBlankEmail = Annotated[str, AfterValidator(_no_blank_y_email)]          
EmailOpcional = Annotated[Optional[str], AfterValidator(_email_opcional)]  
ContrasenaValida = Annotated[str, AfterValidator(_contrasena_valida)]      
ContrasenaOpcional = Annotated[Optional[str], AfterValidator(_contrasena_opcional)] 
Positivo = Annotated[int, AfterValidator(_positivo)]                      
PositivoOCero = Annotated[int, AfterValidator(_positivo_o_cero)]           
PrecioPositivo = Annotated[Decimal, AfterValidator(_precio_positivo)]      
ListaVentaNoVacia = AfterValidator(_lista_no_vacia_venta)                  
