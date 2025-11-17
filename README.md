# Emissions Dashboard

![License](https://img.shields.io/badge/License-MIT-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-18+-61dafb?logo=react)
![TimescaleDB](https://img.shields.io/badge/TimescaleDB-Hypertables-faa21b)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker)

A production-style geospatial analytics experience that visualizes air-quality observations in real time. The dashboard combines a Vite + React client, a FastAPI analytics service, and a TimescaleDB warehouse preloaded with demo datasets. The stack demonstrates how to ingest, aggregate, and present OpenAQ data through a cohesive developer workflow.

---

## Table of contents
1. [Why this project matters](#why-this-project-matters)
2. [Feature tour](#feature-tour)
3. [Implementation blueprint](#implementation-blueprint)
4. [System architecture](#system-architecture)
5. [Getting started](#getting-started)
6. [Running services without Docker](#running-services-without-docker)
7. [Data and API reference](#data-and-api-reference)
8. [Roadmap and future upgrades](#roadmap-and-future-upgrades)
9. [Troubleshooting](#troubleshooting)

---

## Why this project matters
Cities need rapid feedback about particulate concentrations and other pollutants to guide policy. Emissions Dashboard demonstrates how to ingest hourly sensor readings, aggregate them into KPIs, and share the insight through an interactive interface. The repository doubles as a template for full-stack data apps: reproducible infrastructure, modern frontend tooling, and a typed Python backend built for time-series workloads.

## Feature tour
- **Interactive geospatial dashboard** – React, Leaflet, and Recharts combine to render station markers, KPI tiles, and time-series charts with smooth hover states.
- **Analytics-grade backend** – FastAPI exposes parameterized endpoints for stations, raw observations, and hourly aggregates, using SQLAlchemy models and Pydantic schemas for safety.
- **Time-series warehouse** – TimescaleDB hypertables, continuous aggregates, and seed SQL scripts accelerate analytical queries even with large observation volumes.
- **Automated ingestion utilities** – Scripts in `backend/app/ingestion` hydrate the warehouse from OpenAQ, controlled via environment variables such as `INGEST_SINCE`.
- **Docker-first workflow** – `make up` builds the entire stack, attaches logs, and guarantees matching dependencies across machines.
- **Developer ergonomics** – Clear Make targets, `.env` templates, and typed code enable quick onboarding.

## Implementation blueprint
1. **Frontend** – Vite bootstraps a React SPA. Components under `frontend/src/components` render maps, KPI cards, and charts. The API client in `frontend/src/api` wraps Axios and honors the `VITE_API_URL` variable.
2. **Backend** – `backend/app/main.py` assembles routers from `app/routers`. Each router speaks to TimescaleDB through a SQLAlchemy session created in `app/db.py`. Response models in `app/schemas.py` keep the API contract explicit.
3. **Database** – Postgres 15 with TimescaleDB extensions initializes via `db/init/*.sql`. Optional demo data resides in `db/seeds/seed_demo.sql` and loads through `make seed`.
4. **Infrastructure** – `docker-compose.yml` defines `frontend`, `backend`, and `db` services. Environment variables are sourced from `.env`, and `Makefile` convenience targets orchestrate the lifecycle.

## System architecture
```
frontend/ (Vite + React)
├─ src/components   → Map, charts, KPI cards
├─ src/api          → Axios client for FastAPI (default http://localhost:8000)
└─ src/pages        → Dashboard layout

backend/ (FastAPI)
├─ app/main.py      → App factory + router registration
├─ app/routers      → Stations, observations, analytics, health
├─ app/ingestion    → OpenAQ ingestion utilities
├─ app/db.py        → SQLAlchemy session + Timescale connection
└─ app/schemas.py   → Pydantic models

db/
├─ init/            → Timescale/Schema bootstrap scripts
└─ seeds/           → Optional demo data
```
Services communicate over an internal Docker network: the frontend calls the API via `VITE_API_URL`, the backend connects to Postgres via `DATABASE_URL`, and the database exposes TimescaleDB hypertables for analytical queries.

## Getting started
### Prerequisites
- Docker and Docker Compose
- GNU Make
- Node.js 18+ and Python 3.11+ (only for running services outside Docker)

### Quick start with Docker Compose
```bash
cp .env.example .env            # configure credentials + service URLs
make up                         # build + start db, backend, frontend
# API docs → http://localhost:8000/docs
# Web UI   → http://localhost:5173
```
`make up` streams container logs. Press `Ctrl+C` to stop tailing without shutting down the stack. Run `make down` to stop services and clean volumes.

### Seed the demo dataset
```bash
make seed   # loads db/seeds/seed_demo.sql into the running Postgres container
```

### Helpful Make targets
| Command     | Description |
|-------------|-------------|
| `make logs` | Tail all service logs |
| `make api`  | Print the FastAPI docs URL |
| `make web`  | Print the frontend URL |
| `make psql` | Launch a psql shell inside the TimescaleDB container |

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
npm run dev   # serves at http://localhost:5173
```
Configure `VITE_API_URL` in `.env` or `.env.local` if the API runs on a different host/port.

## Data and API reference
### Environment variables
| Variable | Description |
|----------|-------------|
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Timescale/Postgres credentials |
| `DATABASE_URL` | SQLAlchemy connection string used by the API |
| `API_CORS_ORIGINS` | JSON list of allowed origins |
| `VITE_API_URL` | Base URL for the frontend Axios client |
| `INGEST_SINCE` | Optional ISO date for OpenAQ ingestion start |
| `OPENAQ_BASE_URL` | Optional override for the OpenAQ API base URL |

### API endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /` | Service metadata |
| `GET /health` | Health probe for Compose |
| `GET /stations` | List up to 1000 stations with metadata |
| `GET /observations` | Raw observations filtered by `station_id`, `parameter`, `start`, `end`, `limit` |
| `GET /analytics/hourly` | Hourly aggregates for a station and pollutant |

Example request:
```bash
curl "http://localhost:8000/analytics/hourly?station_id=DEMO_1&parameter=pm25"
```
Response snippet:
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

## Roadmap and future upgrades
1. **Live streaming ingestion** – Replace batch imports with Debezium or Kafka Connect to capture measurements continuously.
2. **Alerting and notifications** – Trigger alerts when rolling averages breach thresholds, with integrations for email or webhooks.
3. **User personalization** – Persist favorite stations, saved filters, and per-user KPI layouts via a lightweight auth service.
4. **Offline-first mobile view** – Ship a PWA profile optimized for phones and add caching for recent readings.
5. **Automated testing pipeline** – Add CI workflows that lint the frontend, run backend tests, and validate SQL migrations.

## Troubleshooting
- **Import errors** – Activate the virtual environment before installing backend dependencies.
- **CORS or URL mismatches** – Ensure `VITE_API_URL` matches the FastAPI host, especially when using tunnels or custom domains.
- **Database connectivity** – Confirm `DATABASE_URL` points to the running TimescaleDB container; inspect `make logs` for failures.
- **Seed failures** – The seed script assumes TimescaleDB extensions are loaded; rerun `make up` if initialization did not complete.

Enjoy exploring the emissions data platform.
