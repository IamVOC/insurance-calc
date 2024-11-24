from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, update, and_

from .schemas import DailyTariffsRequest, MaterialTariff, TariffResponse
from .models import Tariff, MaterialRate


async def create_tariff_plans(
    *, tariffs: DailyTariffsRequest, db: AsyncSession
) -> List[TariffResponse]:
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
    res = [
        TariffResponse.model_validate(i, from_attributes=True) for i in inserted_tariffs
    ]
    await db.commit()
    return res


async def update_tariff_plans(
    *, tariff_id: int, rates: List[MaterialTariff], db: AsyncSession
) -> List[MaterialRate]:
    res = []
    for rate in rates:
        stmt = (
            update(MaterialRate)
            .where(
                and_(
                    MaterialRate.tariff_id == tariff_id,
                    MaterialRate.material_type == rate.material_type,
                )
            )
            .values(rate=rate.rate)
            .returning(MaterialRate)
        )
        ret = await db.execute(stmt)
        sc = ret.scalar()
        if sc:
            res.append(sc)
    await db.commit()
    return res


async def delete_tariff_plans(*, tariff_id: int, db: AsyncSession) -> Optional[TariffResponse]:
    stmt = delete(Tariff).where(Tariff.id == tariff_id).returning(Tariff)
    ret = await db.execute(stmt)
    tariff = ret.scalar()
    res = TariffResponse.model_validate(tariff, from_attributes=True) if tariff else None
    await db.commit()
    if res:
        return res
