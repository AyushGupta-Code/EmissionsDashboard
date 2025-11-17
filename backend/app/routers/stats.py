from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text

from ..db import get_db, table

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary")
def get_summary(db=Depends(get_db)):
    stations_table = table("stations")
    observations_table = table("observations")
    window_start = datetime.now(tz=timezone.utc) - timedelta(hours=24)

    query = text(
        f"""
        SELECT
            (SELECT COUNT(*) FROM {stations_table}) AS station_count,
            (SELECT COUNT(*) FROM {observations_table} WHERE time >= :window_start) AS observation_24h
        """
    )

    params = {"window_start": window_start.isoformat()}
    return db.execute(query, params).mappings().one()
