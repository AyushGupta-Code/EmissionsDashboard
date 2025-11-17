from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Text, TIMESTAMP

class Base(DeclarativeBase):
    pass

class Station(Base):
    __tablename__ = "stations"
    __table_args__ = {"schema": "air"}
    station_id: Mapped[str] = mapped_column(String, primary_key=True)
    name:       Mapped[str | None] = mapped_column(Text)
    provider:   Mapped[str | None] = mapped_column(Text)
    country:    Mapped[str | None] = mapped_column(Text)
    city:       Mapped[str | None] = mapped_column(Text)
    latitude:   Mapped[float]
    longitude:  Mapped[float]
    elevation_m:Mapped[float | None]

class Observation(Base):
    __tablename__ = "observations"
    __table_args__ = {"schema": "air"}
    time:        Mapped[str]  = mapped_column(TIMESTAMP(timezone=True), primary_key=True)
    station_id:  Mapped[str]  = mapped_column(String, primary_key=True)
    parameter:   Mapped[str]  = mapped_column(String, primary_key=True)
    unit:        Mapped[str]
    value:       Mapped[float]
    quality:     Mapped[str | None]
    source:      Mapped[str | None]
