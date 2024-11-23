import pytest


@pytest.mark.asyncio
async def test_create_tariff_route(client):
    data = {
        "2020-01-01": [{"type": "Glass", "rate": 0.35}, {"type": "Other", "rate": 0.3}],
        "2020-01-02": [{"type": "Glass", "rate": 0.3}, {"type": "Other", "rate": 0.25}],
    }

    response = await client.post("/tariff", json=data)

    assert response.status_code == 200
    assert response.json()[0]["relevance_date"] == "2020-01-01"
    assert response.json()[1]["relevance_date"] == "2020-01-02"
