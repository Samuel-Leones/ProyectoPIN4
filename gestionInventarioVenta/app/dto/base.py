from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.dto.tipos import FechaHora


class DtoBase(BaseModel):

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class DtoAuditoria(DtoBase):

    estado: bool
    creado: FechaHora
    actualizado: FechaHora


def campos_auditoria(entidad) -> dict:
    return {"estado": entidad.estado, "creado": entidad.creado, "actualizado": entidad.actualizado}
