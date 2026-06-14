FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SCOUTFOOTBALL_ENV=production \
    DATABASE_URL=sqlite:///backend/data/scoutfootball.db \
    STATSBOMB_DATA_DIR=backend/data_sources/statsbomb_open \
    CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

WORKDIR /app

COPY backend/pyproject.toml /app/backend/pyproject.toml
COPY backend/app /app/backend/app
COPY backend/scripts /app/backend/scripts

WORKDIR /app/backend

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
