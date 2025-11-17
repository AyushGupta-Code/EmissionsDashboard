from fastapi import APIRouter, Depends
from sqlalchemy import text
from ..db import get_db, table

router = APIRouter(prefix="/stations", tags=["stations"])

@router.get("")
def list_stations(db=Depends(get_db)):
    stations_table = table("stations")
    q = text(
        f"SELECT station_id, name, provider, country, city, latitude, longitude FROM {stations_table} ORDER BY station_id LIMIT 1000"
    )
    rows = db.execute(q).mappings().all()
    return list(rows)
