# Emissions Dashboard

A full-stack geospatial analytics demo that surfaces air-quality observations on an interactive map, renders time-series charts, and exposes a FastAPI analytics backend backed by TimescaleDB continuous aggregates.

## Features
- **Interactive dashboard** – React + Leaflet map, KPI cards, and Recharts visualizations.
- **FastAPI backend** – Parameterized endpoints for stations, raw observations, and hourly aggregates.
- **TimescaleDB storage** – Hypertables, continuous aggregates, and seed/demo data for development.
- **Docker-first workflow** – `docker compose` stack that brings up the database, API, and frontend in a single command.
- **Ingestion utilities** – Scripts for pulling OpenAQ data and loading it into the warehouse.

## Architecture
```
frontend/ (Vite + React)
├─ src/components   → Map, charts, KPI cards
├─ src/api          → Axios client targeting the API (default http://localhost:8000)
└─ src/pages        → Dashboard layout

backend/ (FastAPI)
├─ app/main.py      → FastAPI app + routers
├─ app/routers      → Stations, observations, analytics, health
├─ app/ingestion    → OpenAQ ingestion utilities
├─ app/db.py        → SQLAlchemy session + Timescale connection
└─ app/schemas.py   → Pydantic response models

db/
├─ init/            → Timescale/Schema bootstrap scripts mounted into Postgres
└─ seeds/           → Optional demo data (see `make seed`)
```

Services communicate over the internal Docker network:
- `frontend` → calls the API using `VITE_API_URL` (defaults to `http://localhost:8000`).
- `backend` → connects to Postgres using `DATABASE_URL`.
- `db` → TimescaleDB (Postgres 15) with hypertables defined in `db/init`.

## Prerequisites
- Docker & Docker Compose
- Make (for convenience targets)
- Node.js ≥ 18 and Python ≥ 3.11 (only needed for running services outside Docker)

## Quick start (Docker Compose)
```bash
cp .env.example .env            # configure credentials + service URLs
make up                         # builds + starts db, backend, frontend
# API docs → http://localhost:8000/docs
# Web UI   → http://localhost:5173
```
The `make up` target streams the container logs. Use `Ctrl+C` to stop tailing without killing the stack. Run `make down` to stop and clean volumes.

### Database seed
A small demo dataset is bundled. After the stack is running:
```bash
make seed   # loads db/seeds/seed_demo.sql into the running Postgres container
```

### Useful helper targets
| Command     | Description |
|-------------|-------------|
| `make logs` | Follow the tail of all service logs |
| `make api`  | Prints a reminder for the FastAPI docs URL |
| `make web`  | Prints a reminder for the frontend URL |
| `make psql` | Open a psql shell inside the TimescaleDB container |

## Running services without Docker
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/emissions"
export API_CORS_ORIGINS='["http://localhost:5173"]'
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev   # http://localhost:5173 by default
```
Set `VITE_API_URL` in `.env` (or `.env.local`) if the API is not running on the default address.

## Environment variables
| Variable | Description |
|----------|-------------|
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Provisioned Timescale/Postgres credentials |
| `DATABASE_URL` | SQLAlchemy connection string used by the API |
| `API_CORS_ORIGINS` | JSON list of allowed origins for the API |
| `VITE_API_URL` | Base URL for the frontend Axios client |
| `INGEST_SINCE` | (Optional) ISO date for the OpenAQ ingestion starting point |
| `OPENAQ_BASE_URL` | (Optional) Override for the OpenAQ API base URL |

## API overview
All endpoints return JSON and support CORS.

| Endpoint | Description |
|----------|-------------|
| `GET /` | Basic service info |
| `GET /health` | Health probe used by docker compose |
| `GET /stations` | List of stations (max 1000) with metadata |
| `GET /observations` | Filterable raw observations (`station_id`, `parameter`, `start`, `end`, `limit`) |
| `GET /analytics/hourly` | Hourly aggregates for a station + parameter, optional `start`/`end` window |

Example hourly request:
```
curl "http://localhost:8000/analytics/hourly?station_id=DEMO_1&parameter=pm25"
```
Response payload:
```json
[
  {
    "time": "2024-05-01T10:00:00+00:00",
    "station_id": "DEMO_1",
    "parameter": "pm25",
    "unit": "µg/m3",
    "avg_value": 8.14,
    "min_value": 4.08,
    "max_value": 14.22,
    "n": 12
  }
]
```

## Ingestion utilities
`backend/app/ingestion/ingest_openaq.py` contains helper functions to pull historical measurements from the OpenAQ API. Configure `INGEST_SINCE` and `OPENAQ_BASE_URL` in `.env`, then run the script inside the backend container (or your virtual environment) to hydrate the database with real data.

## Testing & troubleshooting
- Backend: add API tests with `pytest` (not bundled) or use `httpx` against `http://localhost:8000`.
- Frontend: run `npm run lint` and `npm run test` as desired (no tests are currently included).

Common pitfalls:
- **Import errors** – ensure you installed backend dependencies inside the active virtual environment.
- **CORS/URL mismatches** – confirm `VITE_API_URL` matches where FastAPI is exposed, especially if tunneling through Docker Desktop.
- **Database connectivity** – the backend expects Timescale/Postgres to be reachable via the `DATABASE_URL` string; check `make logs` if migrations/seeds fail.

Enjoy exploring the emissions data!
