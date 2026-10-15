from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional

import jwt

from app.config.configuracion import configuracion
from app.model.usuario import Usuario


class ServicioJwt:
    def __init__(self, secreto: str, minutos_expiracion: int):
        self._secreto = secreto
        self.minutos_expiracion = minutos_expiracion
        self._clave_firma: Optional[bytes] = None
        self._algoritmo: Optional[str] = None

    def _obtener_clave(self) -> tuple[bytes, str]:
        """Equivalente a Keys.hmacShaKeyFor(): el algoritmo HS256/384/512 depende del largo de la clave."""
        if self._clave_firma is None:
            clave = self._secreto.encode("utf-8")
            bits = len(clave) * 8
            if bits < 256:
                raise ValueError("La clave JWT debe tener al menos 256 bits (32 caracteres)")
            self._clave_firma = clave
            self._algoritmo = "HS512" if bits >= 512 else "HS384" if bits >= 384 else "HS256"
        return self._clave_firma, self._algoritmo

    def generar_token(self, usuario: Usuario) -> str:
        clave, algoritmo = self._obtener_clave()
        ahora = datetime.now().astimezone()
        expiracion = ahora + timedelta(minutes=self.minutos_expiracion)
        claims = {
            "sub": usuario.correo,
            "rol": usuario.rol.nombre,
            "usuarioId": usuario.id,
            "iat": int(ahora.timestamp()),
            "exp": int(expiracion.timestamp()),
        }
        return jwt.encode(claims, clave, algorithm=algoritmo)

    def extraer_correo(self, token: str) -> Optional[str]:
        claims = self._extraer_todos_los_claims(token)
        return claims.get("sub") if claims else None

    def es_token_valido(self, token: str) -> bool:
        try:
            return self._extraer_todos_los_claims(token) is not None
        except Exception:
            return False

    def _extraer_todos_los_claims(self, token: str) -> Optional[dict]:
        try:
            clave, algoritmo = self._obtener_clave()
            return jwt.decode(
                token,
                clave,
                algorithms=[algoritmo],
                options={"require": ["exp"], "verify_iat": False},
            )
        except Exception:
            return None


@lru_cache(maxsize=1)
def obtener_servicio_jwt() -> ServicioJwt:
    return ServicioJwt(configuracion.jwt_secreto, configuracion.jwt_minutos_expiracion)
