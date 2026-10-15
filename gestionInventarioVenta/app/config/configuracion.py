import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _entero(nombre: str, por_defecto: int) -> int:
    return int(os.getenv(nombre, str(por_defecto)))


@dataclass(frozen=True)
class Configuracion:
    nombre_aplicacion: str = "gestion-inventario-ventas"

    database_url: str = os.getenv("DATABASE_URL", "").strip()
    db_usuario: str = os.getenv("DB_USERNAME", "postgres")
    db_contrasena: str = os.getenv("DB_PASSWORD", "")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_puerto: int = _entero("DB_PORT", 5432)
    db_nombre: str = os.getenv("DB_NAME", "gestion_inventario_ventas")
    mostrar_sql: bool = os.getenv("MOSTRAR_SQL", "false").lower() == "true"

    jwt_secreto: str = os.getenv("JWT_SECRET", "change-this-secret-in-production-min-256-bits-long")
    jwt_minutos_expiracion: int = _entero("JWT_EXPIRATION_MINUTES", 30)

    semilla_correo: str = os.getenv("SEED_SUPERUSER_EMAIL", "superadmin@accesoriosmoto.com")
    semilla_contrasena: str = os.getenv("SEED_SUPERUSER_PASSWORD", "SuperAdmin123")

    zona_horaria: str = os.getenv("ZONA_HORARIA", "America/Bogota")

    catalogo_motos_url: str = os.getenv("CATALOGO_MOTOS_URL", "http://localhost:4000").strip().rstrip("/")
    catalogo_motos_timeout: float = float(os.getenv("CATALOGO_MOTOS_TIMEOUT_SEGUNDOS", "5"))

    puerto_servidor: int = _entero("SERVER_PORT", 8080)


configuracion = Configuracion()
