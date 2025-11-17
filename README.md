# Emissions Dashboard

Data‑intensive geospatial/temporal analytics app.

## Stack
- React + Vite + TypeScript
- Leaflet + Recharts
- FastAPI
- TimescaleDB (Postgres hypertables + continuous aggregates)
- Docker Compose

## Quick start
```bash
cp .env.example .env
make up
# API docs → http://localhost:8000/docs
# Web app  → http://localhost:5173
```
A small demo seed is included. To pull real OpenAQ data, adjust `INGEST_SINCE` in `.env`.
