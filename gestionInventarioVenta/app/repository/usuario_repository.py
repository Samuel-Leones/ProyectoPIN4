from typing import Optional

from sqlalchemy import select

from app.model.usuario import Usuario
from app.repository.repositorio_jpa import RepositorioJpa


class UsuarioRepository(RepositorioJpa[Usuario]):
    modelo = Usuario

    def find_by_correo(self, correo: str) -> Optional[Usuario]:
        return self.db.scalars(select(Usuario).where(Usuario.correo == correo).limit(1)).first()

    def exists_by_correo(self, correo: str) -> bool:
        return self.db.scalar(select(Usuario.id).where(Usuario.correo == correo).limit(1)) is not None

    def exists_by_rol_id_and_estado_true(self, rol_id: int) -> bool:
        consulta = select(Usuario.id).where(Usuario.rol_id == rol_id, Usuario.estado.is_(True)).limit(1)
        return self.db.scalar(consulta) is not None
