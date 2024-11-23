from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from .schemas import DailyTariffsRequest, TariffResponse
import src.tariff.service as tariff_service


router = APIRouter(prefix="/tariff", tags=["Tariff"]) # pragma: no cover


@router.post("", status_code=status.HTTP_200_OK, response_model=List[TariffResponse]) # pragma: no cover
async def create_tariff_plans(
    tariffs: DailyTariffsRequest, db: AsyncSession = Depends(get_db)
):
    res = await tariff_service.create_tariff_plans(db=db, tariffs=tariffs)
    return res

