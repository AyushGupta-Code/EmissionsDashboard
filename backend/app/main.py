from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routers import health, stations, observations, analytics

app = FastAPI(title="Emissions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Emissions API"}

app.include_router(health.router)
app.include_router(stations.router)
app.include_router(observations.router)
app.include_router(analytics.router)
