import datetime
import pytest
from sqlalchemy import and_, insert, select

from src.tariff.service import delete_tariff_plans, update_tariff_plans
from src.tariff.schemas import MaterialTariff
from src.tariff.models import MaterialRate, Tariff


@pytest.mark.asyncio
async def test_delete_tariffs(session):
    raw_res = await session.execute(
        insert(Tariff)
        .values([{"relevance_date": datetime.date(2020, 1, 1)}])
        .returning(Tariff.id)
    )
    tariff_id = raw_res.scalar()
    await session.execute(
        insert(MaterialRate).values(
            [{"material_type": "Glass", "rate": 0.3, "tariff_id": tariff_id}]
        )
    )

    res = await delete_tariff_plans(tariff_id=tariff_id, db=session)

    scres = await session.scalars(select(Tariff).where(Tariff.id == tariff_id))
    items = scres.all()
    assert res
    assert not items


@pytest.mark.asyncio
async def test_update_tariffs(session):
    raw_res = await session.execute(
        insert(Tariff)
        .values([{"relevance_date": datetime.date(2020, 1, 1)}])
        .returning(Tariff.id)
    )
    tariff_id = raw_res.scalar()
    await session.execute(
        insert(MaterialRate).values(
            [{"material_type": "Glass", "rate": 0.3, "tariff_id": tariff_id}]
        )
    )

    await update_tariff_plans(
        tariff_id=tariff_id,
        rates=[
            MaterialTariff.model_validate(
                {
                    "type": "Glass",
                    "rate": 0.4,
                    "relevance_date": datetime.date(2020, 1, 1),
                }
            )
        ],
        db=session,
    )

    scres = await session.scalars(
        select(MaterialRate).where(
            and_(
                MaterialRate.tariff_id == tariff_id,
                MaterialRate.material_type == "Glass",
            )
        )
    )
    items = scres.all()
    assert items[0].rate == 0.4
