from datetime import date
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from src.db import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    relevance_date: Mapped[date] = mapped_column(index=True, unique=True)

    rates: Mapped[List["MaterialRate"]] = relationship(
        back_populates="tariff", passive_deletes=True
    )


class MaterialRate(Base):
    __tablename__ = "material_rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    material_type: Mapped[str]
    rate: Mapped[float]
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id", ondelete="CASCADE"))

    tariff: Mapped["Tariff"] = relationship(back_populates="rates")

    __table_args__ = (
        Index(
            "ix_material_rates_tariff_id_material_type",
            "tariff_id",
            "material_type",
            unique=True,
        ),
    )
