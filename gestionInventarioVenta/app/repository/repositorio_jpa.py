from typing import Generic, Optional, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

T = TypeVar("T")


class RepositorioJpa(Generic[T]):
    modelo: type[T]

    def __init__(self, db: Session):
        self.db = db

    def save(self, entidad: T) -> T:
        try:
            self.db.add(entidad)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        
        self.db.refresh(entidad)
        return entidad

    def find_by_id(self, id: int) -> Optional[T]:
        return self.db.get(self.modelo, id)

    def find_all(self) -> list[T]:
        return list(self.db.scalars(select(self.modelo).order_by(self.modelo.id)).all())

    def find_all_by_estado_true(self) -> list[T]:
        consulta = select(self.modelo).where(self.modelo.estado.is_(True)).order_by(self.modelo.id)
        return list(self.db.scalars(consulta).all())

    def count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(self.modelo)) or 0

    def count_by_estado_true(self) -> int:
        consulta = select(func.count()).select_from(self.modelo).where(self.modelo.estado.is_(True))
        return self.db.scalar(consulta) or 0
