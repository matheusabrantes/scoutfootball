from fastapi import FastAPI

from app.api.routes.compare import router as compare_router
from app.api.routes.data_sources import router as data_sources_router
from app.api.routes.health import router as health_router
from app.api.routes.leagues import router as leagues_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.players import router as players_router
from app.api.routes.rankings import router as rankings_router
from app.api.routes.seasons import router as seasons_router
from app.api.routes.teams import router as teams_router

app = FastAPI(title="ScoutFootball API", version="0.1.0")

app.include_router(health_router)
app.include_router(leagues_router)
app.include_router(players_router)
app.include_router(rankings_router)
app.include_router(compare_router)
app.include_router(metrics_router)
app.include_router(seasons_router)
app.include_router(teams_router)
app.include_router(data_sources_router)
