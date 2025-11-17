from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from ..db import get_db, table

router = APIRouter(prefix="/observations", tags=["observations"])

@router.get("")
def list_observations(
    station_id: str | None = None,
    parameter: str | None = None,
    start: str | None = Query(None, description="ISO8601 timestamp"),
    end: str | None = Query(None, description="ISO8601 timestamp"),
    limit: int = 1000,
    db=Depends(get_db),
):
    observations_table = table("observations")
    parts = [
        f"SELECT time, station_id, parameter, unit, value, quality, source FROM {observations_table} WHERE 1=1"
    ]
    params = {}
    if station_id:
        parts.append("AND station_id = :station_id")
        params["station_id"] = station_id
    if parameter:
        parts.append("AND parameter = :parameter")
        params["parameter"] = parameter
    if start:
        parts.append("AND time >= :start")
        params["start"] = start
    if end:
        parts.append("AND time <= :end")
        params["end"] = end
    parts.append("ORDER BY time DESC LIMIT :limit")
    params["limit"] = limit
    q = text("\n".join(parts))
    return list(db.execute(q, params).mappings().all())
