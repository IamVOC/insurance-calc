import datetime
import pytest

from src.tariff.service import create_tariff_plans
from src.tariff.schemas import DailyTariffsRequest


@pytest.mark.asyncio
async def test_create_tariffs(session):
    data = {
        "2020-01-01": [{"type": "Glass", "rate": 0.35}, {"type": "Other", "rate": 0.3}],
        "2020-01-02": [{"type": "Glass", "rate": 0.3}, {"type": "Other", "rate": 0.25}],
    }

    res = await create_tariff_plans(
        tariffs=DailyTariffsRequest.model_validate(data), db=session
    )

    assert res[0].relevance_date == datetime.date(2020, 1, 1)
    assert res[1].relevance_date == datetime.date(2020, 1, 2)
