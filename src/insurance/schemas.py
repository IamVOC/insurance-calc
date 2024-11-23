from datetime import date
from pydantic import BaseModel


class CargoRequest(BaseModel):
    cargo_type: str
    declared_cost: float
    cargo_date: date


class InsuranceResponse(BaseModel):
    insurance_amount: float
