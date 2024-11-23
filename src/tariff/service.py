from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from .schemas import DailyTariffsRequest, TariffResponse
from .models import Tariff, MaterialRate


async def create_tariff_plans(*, tariffs: DailyTariffsRequest, db: AsyncSession) -> List[TariffResponse]:
    insert_tariffs_stmt = (
        insert(Tariff)
        .values([{"relevance_date": date} for date in tariffs.root.keys()])
        .returning(Tariff)
    )
    raw_tariffs = await db.execute(insert_tariffs_stmt)
    inserted_tariffs = raw_tariffs.scalars().all()
    insert_rates_stmt = insert(MaterialRate).values(
        [
            {
                "material_type": material_rates.material_type,
                "rate": material_rates.rate,
                "tariff_id": tariff.id,
            }
            for tariff, values in zip(inserted_tariffs, tariffs.root.values())
            for material_rates in values
        ]
    )
    await db.execute(insert_rates_stmt)
    res = [TariffResponse.model_validate(i, from_attributes=True) for i in inserted_tariffs]
    await db.commit()
    return res
