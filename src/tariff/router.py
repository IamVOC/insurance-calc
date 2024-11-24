import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from .schemas import DailyTariffsRequest, TariffResponse, MaterialTariff
import src.tariff.service as tariff_service
from src.publisher.service import produce_message
from src.publisher.utils import generate_kafka_message


router = APIRouter(prefix="/tariff", tags=["Tariff"])  # pragma: no cover


@router.post(
    "", status_code=status.HTTP_200_OK, response_model=List[TariffResponse]
)  # pragma: no cover
async def create_tariff_plans(
        tariffs: DailyTariffsRequest, bt: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    res = await tariff_service.create_tariff_plans(db=db, tariffs=tariffs)
    bt.add_task(produce_message, generate_kafka_message('add'))
    return res


@router.put("/{tariffID}", status_code=status.HTTP_204_NO_CONTENT)  # pragma: no cover
async def update_tariff_plans(
        tariffID: int, rates: List[MaterialTariff], bt: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    res = await tariff_service.update_tariff_plans(
        db=db, tariff_id=tariffID, rates=rates
    )
    if not res:
        raise HTTPException(status_code=404, detail="No tariff was found")
    bt.add_task(produce_message, generate_kafka_message('update'))
    


@router.delete(
    "/{tariffID}", status_code=status.HTTP_204_NO_CONTENT
)  # pragma: no cover
async def delete_tariff_plans(tariffID: int, bt: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    res = await tariff_service.delete_tariff_plans(db=db, tariff_id=tariffID)
    if not res:
        raise HTTPException(status_code=404, detail="No tariff was found")
    bt.add_task(produce_message, generate_kafka_message('delete'))
