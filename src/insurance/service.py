from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CargoRequest, InsuranceResponse
from src.tariff.models import Tariff, MaterialRate


async def calculate_insurance(
    *, cargo: CargoRequest, db: AsyncSession
) -> InsuranceResponse | None:
    select_stmt = (
        select(MaterialRate.rate * cargo.declared_cost)
        .join(Tariff, Tariff.id == MaterialRate.tariff_id)
        .where(
            and_(
                Tariff.relevance_date == cargo.cargo_date,
                MaterialRate.material_type == cargo.cargo_type,
            )
        )
    )
    raw_insurance = await db.execute(select_stmt)
    insurance = raw_insurance.scalar()
    if insurance:
        return InsuranceResponse(insurance_amount=insurance)
