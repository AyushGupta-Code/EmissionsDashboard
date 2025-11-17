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
    """
    Return hourly aggregates for a station/parameter between optional start/end.
    """

    # Build WHERE conditions dynamically so we don't send NULL parameters
    conditions = [
        "station_id = :station_id",
        "parameter  = :parameter",
    ]
    params: dict[str, object] = {
        "station_id": station_id,
        "parameter": parameter,
    }

    if start is not None:
        conditions.append("bucket >= :start")
        params["start"] = start

    if end is not None:
        conditions.append("bucket <= :end")
        params["end"] = end

    where_clause = " AND ".join(conditions)

    sql = text(f"""
        SELECT
            bucket AS time,
            station_id,
            parameter,
            unit,
            avg_value,
            min_value,
            max_value,
            n
        FROM air.obs_hourly
        WHERE {where_clause}
        ORDER BY time
    """)

    rows = db.execute(sql, params).mappings().all()
    return [HourlyResponse(**row) for row in rows]
