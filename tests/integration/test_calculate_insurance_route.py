import pytest


@pytest.mark.asyncio
async def test_create_tariff_route(insurance_client):
    data = {"cargo_type": "Glass", "declared_cost": 100, "cargo_date": "2020-01-01"}

    response = await insurance_client.get("/insurance", params=data)

    assert response.status_code == 200
