from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from .schemas import DailyTariffsRequest, TariffResponse, MaterialTariff
import src.tariff.service as tariff_service


router = APIRouter(prefix="/tariff", tags=["Tariff"])  # pragma: no cover


@router.post(
    "", status_code=status.HTTP_200_OK, response_model=List[TariffResponse]
)  # pragma: no cover
async def create_tariff_plans(
    tariffs: DailyTariffsRequest, db: AsyncSession = Depends(get_db)
):
    res = await tariff_service.create_tariff_plans(db=db, tariffs=tariffs)
    return res


@router.put("/{tariffID}", status_code=status.HTTP_204_NO_CONTENT)  # pragma: no cover
async def update_tariff_plans(
    tariffID: int, rates: List[MaterialTariff], db: AsyncSession = Depends(get_db)
):
    res = await tariff_service.update_tariff_plans(
        db=db, tariff_id=tariffID, rates=rates
    )
    if not res:
        raise HTTPException(status_code=404, detail="No tariff was found")


@router.delete(
    "/{tariffID}", status_code=status.HTTP_204_NO_CONTENT
)  # pragma: no cover
async def delete_tariff_plans(tariffID: int, db: AsyncSession = Depends(get_db)):
    res = await tariff_service.delete_tariff_plans(db=db, tariff_id=tariffID)
    if not res:
        raise HTTPException(status_code=404, detail="No tariff was found")
