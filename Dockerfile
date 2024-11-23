FROM python:3.11-alpine AS builder

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.3.2 \
    && poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-interaction --no-ansi

FROM python:3.11-alpine
WORKDIR /app

COPY --from=builder /app /app
COPY ./src ./src
ENV PYTHONPATH="/app"

CMD ["/app/.venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
