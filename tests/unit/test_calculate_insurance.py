from datetime import date
import pytest
from sqlalchemy import insert

from src.tariff.models import MaterialRate, Tariff
from src.insurance.schemas import CargoRequest
from src.insurance.service import calculate_insurance


@pytest.mark.asyncio
async def test_calculate_insurance(session):
    data = {"cargo_type": "Glass", "declared_cost": 100, "cargo_date": date(2020, 1, 1)}
    cargo = CargoRequest.model_validate(data)
    raw_res = await session.execute(
        insert(Tariff).values([{"relevance_date": date(2020,1,1)}]).returning(Tariff.id)
    )
    tariff_id = raw_res.scalar()
    await session.execute(
        insert(MaterialRate).values(
            [{"material_type": "Glass", "rate": 0.3, "tariff_id": tariff_id}]
        )
    )

    insurance = await calculate_insurance(cargo=cargo, db=session)

    assert insurance
    assert insurance.insurance_amount == 30

@pytest.mark.asyncio
async def test_insurance_tariff_nf(session):
    data = {"cargo_type": "Glass", "declared_cost": 100, "cargo_date": date(2020, 1, 1)}
    cargo = CargoRequest.model_validate(data)

    insurance = await calculate_insurance(cargo=cargo, db=session)

    assert insurance is None

