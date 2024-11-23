from datetime import date
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import mapped_column, Mapped

from src.db import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    relevance_date: Mapped[date] = mapped_column(index=True)


class MaterialRate(Base):
    __tablename__ = "material_rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    material_type: Mapped[str]
    rate: Mapped[float]
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))

    __table_args__ = (
        Index(
            "ix_material_rates_tariff_id_material_type",
            "tariff_id",
            "material_type",
            unique=True,
        ),
    )
