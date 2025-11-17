CREATE SCHEMA IF NOT EXISTS air;

CREATE TABLE IF NOT EXISTS air.stations (
  station_id TEXT PRIMARY KEY,
  name TEXT,
  provider TEXT,
  country TEXT,
  city TEXT,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  elevation_m DOUBLE PRECISION,
  first_seen timestamptz,
  last_seen timestamptz
);

CREATE TABLE IF NOT EXISTS air.observations (
  time timestamptz NOT NULL,
  station_id TEXT NOT NULL REFERENCES air.stations(station_id),
  parameter TEXT NOT NULL,
  unit TEXT NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  quality TEXT,
  source TEXT,
  PRIMARY KEY (time, station_id, parameter)
);

SELECT create_hypertable('air.observations', by_range('time'), if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_obs_station_time ON air.observations (station_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_obs_param_time   ON air.observations (parameter, time DESC);
