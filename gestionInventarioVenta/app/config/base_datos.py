from datetime import datetime
from typing import Iterator

from sqlalchemy import BigInteger, Boolean, DateTime, create_engine, func, text, true
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.config.configuracion import configuracion

TipoId = BigInteger


class Base(DeclarativeBase):
    pass


class CamposComunes:
    estado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=true(), sort_order=1000
    )
    creado: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), sort_order=1001
    )
    actualizado: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), sort_order=1002
    )


def _url_base_datos() -> URL:
    if configuracion.database_url:
        url = make_url(configuracion.database_url)
        if url.drivername in ("postgres", "postgresql"):
            url = url.set(drivername="postgresql+psycopg2")
        return url
    return URL.create(
        "postgresql+psycopg2",
        username=configuracion.db_usuario,
        password=configuracion.db_contrasena or None,
        host=configuracion.db_host,
        port=configuracion.db_puerto,
        database=configuracion.db_nombre,
    )


motor = create_engine(
    _url_base_datos(),
    echo=configuracion.mostrar_sql,
    pool_pre_ping=True,  
    pool_recycle=300,
    connect_args={"keepalives": 1, "keepalives_idle": 30, "keepalives_interval": 10, "keepalives_count": 5},
)
SesionLocal = sessionmaker(bind=motor, autoflush=True, expire_on_commit=False)

_FUNCION_ACTUALIZADO = """
CREATE OR REPLACE FUNCTION fn_actualizar_campo_actualizado() RETURNS trigger AS $$
BEGIN
    NEW.actualizado = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql
"""


def inicializar_esquema() -> None:
    """Crea las tablas que falten y los triggers que mantienen el campo 'actualizado'."""
    from app import model  
    Base.metadata.create_all(motor)

    with motor.begin() as conexion:
        conexion.execute(text(_FUNCION_ACTUALIZADO))
        for tabla in Base.metadata.sorted_tables:
            if "actualizado" in tabla.c:
                trigger = f"trg_{tabla.name}_actualizado"
                conexion.execute(text(f'DROP TRIGGER IF EXISTS {trigger} ON "{tabla.name}"'))
                conexion.execute(
                    text(
                        f'CREATE TRIGGER {trigger} BEFORE UPDATE ON "{tabla.name}" '
                        f"FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado()"
                    )
                )


def obtener_sesion() -> Iterator[Session]:
    """Una sesión por petición."""
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
