from fastapi import FastAPI

from src.config import settings
from src.tariff.router import router as tariff_router
from src.insurance.router import router as insurance_router


app = FastAPI(root_path="/api/v1")

if settings.ENVIRONMENT not in ("local", "production"):
    app.openapi_url = None

app.include_router(tariff_router)
app.include_router(insurance_router)
