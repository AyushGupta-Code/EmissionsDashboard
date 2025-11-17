# from datetime import datetime
# from typing import Optional

# from fastapi import APIRouter, Depends
# from sqlalchemy import text
# from sqlalchemy.orm import Session

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session as DbSession

from ..db import get_db
from ..schemas import HourlyResponse

router = APIRouter()


@router.get("/analytics/hourly", response_model=list[HourlyResponse])
def hourly(
    station_id: str,
    parameter: str,
    start: datetime | None = None,
    end: datetime | None = None,
    db: DbSession = Depends(get_db),
) -> list[HourlyResponse]:
    """Return hourly aggregates for a station/parameter between optional start/end."""

    conditions = [
        "station_id = :station_id",
        "parameter  = :parameter",
    ]
    params: dict[str, object] = {
        "station_id": station_id,
        "parameter": parameter,
    }

    if start is not None:
        conditions.append("time >= :start")
        params["start"] = start

    if end is not None:
        conditions.append("time <= :end")
        params["end"] = end

    where_clause = " AND ".join(conditions)

    sql = text(
        f"""
        SELECT
            date_trunc('hour', time) AS time,
            station_id,
            parameter,
            MIN(unit)        AS unit,
            AVG(value)       AS avg_value,
            MIN(value)       AS min_value,
            MAX(value)       AS max_value,
            COUNT(*)         AS n
        FROM air.observations
        WHERE {where_clause}
        GROUP BY 1, 2, 3
        ORDER BY time
        """
    )

    rows = db.execute(sql, params).mappings().all()
    return [HourlyResponse(**row) for row in rows]
