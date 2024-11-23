from datetime import date
from typing import Dict, List
from pydantic import BaseModel, RootModel, Field, ConfigDict


class MaterialTariff(BaseModel):
    material_type: str = Field(alias="type")
    rate: float


class DailyTariffsRequest(RootModel):
    root: Dict[date, List[MaterialTariff]]


class TariffResponse(BaseModel):
    tariff_id: int = Field(alias="id")
    relevance_date: date

    model_config = ConfigDict(from_attributes=True)
