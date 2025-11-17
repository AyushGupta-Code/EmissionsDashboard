from pydantic import BaseModel
from datetime import datetime

class StationOut(BaseModel):
    station_id: str
    name: str | None
    provider: str | None
    country: str | None
    city: str | None
    latitude: float
    longitude: float

class ObservationOut(BaseModel):
    time: datetime
    station_id: str
    parameter: str
    unit: str
    value: float
    quality: str | None
    source: str | None
