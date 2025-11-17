"""Database helpers.

This module now supports two modes of operation:

1.  Use the ``DATABASE_URL`` connection string (PostgreSQL in production).
2.  When the target database is unavailable we transparently fall back to a
    SQLite database that is automatically created with a few demo rows.  The
    fallback keeps the API responsive for local development and automated
    checks without requiring a running PostgreSQL instance.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from .core.config import settings

LOGGER = logging.getLogger(__name__)
_DEMO_SQLITE_PATH = Path(__file__).resolve().parent / "demo.db"


def _build_engine(url: str):
    return create_engine(url, pool_pre_ping=True, future=True)


def _bootstrap_sqlite_engine():
    """Create a SQLite engine pre-populated with demo data."""

    engine = _build_engine(f"sqlite+pysqlite:///{_DEMO_SQLITE_PATH}")

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS stations (
                    station_id  TEXT PRIMARY KEY,
                    name        TEXT,
                    provider    TEXT,
                    country     TEXT,
                    city        TEXT,
                    latitude    REAL NOT NULL,
                    longitude   REAL NOT NULL,
                    elevation_m REAL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS observations (
                    time       TEXT NOT NULL,
                    station_id TEXT NOT NULL,
                    parameter  TEXT NOT NULL,
                    unit       TEXT NOT NULL,
                    value      REAL NOT NULL,
                    quality    TEXT,
                    source     TEXT,
                    PRIMARY KEY (time, station_id, parameter)
                )
                """
            )
        )

        # Seed predictable demo data so the UI has something to render.
        conn.execute(text("DELETE FROM stations"))
        conn.execute(text("DELETE FROM observations"))

        conn.execute(
            text(
                """
                INSERT INTO stations (station_id, name, provider, country, city, latitude, longitude, elevation_m)
                VALUES (:station_id, :name, :provider, :country, :city, :latitude, :longitude, :elevation_m)
                """
            ),
            {
                "station_id": "DEMO_1",
                "name": "Demo Station 1",
                "provider": "demo",
                "country": "US",
                "city": "Raleigh",
                "latitude": 35.7796,
                "longitude": -78.6382,
                "elevation_m": 96.0,
            },
        )

        now = datetime.now(tz=timezone.utc)
        samples = []
        for idx, value in enumerate((14.2, 18.9, 12.1)):
            samples.append(
                {
                    "time": (now - timedelta(hours=2 - idx)).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "station_id": "DEMO_1",
                    "parameter": "pm25",
                    "unit": "µg/m³",
                    "value": value,
                    "quality": "ok",
                    "source": "demo",
                }
            )

        conn.execute(
            text(
                """
                INSERT INTO observations (time, station_id, parameter, unit, value, quality, source)
                VALUES (:time, :station_id, :parameter, :unit, :value, :quality, :source)
                """
            ),
            samples,
        )

    settings.database_schema = None  # type: ignore[attr-defined]
    LOGGER.warning(
        "Falling back to built-in SQLite demo DB at %s", _DEMO_SQLITE_PATH
    )
    return engine


def _create_engine_with_fallback():
    engine = _build_engine(settings.database_url)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except OperationalError as exc:  # pragma: no cover - exercised during runtime
        LOGGER.error("Database connection failed: %s", exc)
        return _bootstrap_sqlite_engine()


engine = _create_engine_with_fallback()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def table(name: str) -> str:
    """Return a fully-qualified table name respecting the configured schema."""

    if settings.database_schema:
        return f"{settings.database_schema}.{name}"
    return name
