from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.db import get_db
from .schemas import CargoRequest, InsuranceResponse
import src.insurance.service as insurance_service


router = APIRouter(prefix="/insurance", tags=["Insurance"])  # pragma: no cover


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=InsuranceResponse
)  # pragma: no cover
async def get_calculated_insurance(
    cargo: Annotated[CargoRequest, Query()], db: AsyncSession = Depends(get_db)
):
    res = await insurance_service.calculate_insurance(cargo=cargo, db=db)
    if not res:
        raise HTTPException(
            status_code=404, detail="No tariff was found for given data and cargo type"
        )
    return res
