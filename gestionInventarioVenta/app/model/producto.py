from decimal import Decimal
from typing import Optional

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base_datos import Base, CamposComunes, TipoId
from app.model.categoria import Categoria
from app.model.proveedor import Proveedor


class Producto(CamposComunes, Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(TipoId, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    codigo: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    categoria_id: Mapped[int] = mapped_column(TipoId, ForeignKey("categorias.id"), nullable=False)
    proveedor_id: Mapped[Optional[int]] = mapped_column(TipoId, ForeignKey("proveedores.id"), nullable=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    stock_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stock_minimo: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    categoria: Mapped[Categoria] = relationship(lazy="select")
    proveedor: Mapped[Optional[Proveedor]] = relationship(lazy="select")
