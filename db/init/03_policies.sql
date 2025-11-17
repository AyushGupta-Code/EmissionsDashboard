ALTER TABLE air.observations SET (timescaledb.compress, timescaledb.compress_segmentby = 'station_id,parameter');
SELECT add_compression_policy('air.observations', INTERVAL '30 days');
SELECT add_retention_policy('air.observations', INTERVAL '365 days');

CREATE MATERIALIZED VIEW IF NOT EXISTS air.obs_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  station_id,
  parameter,
  unit,
  avg(value) AS avg_value,
  min(value) AS min_value,
  max(value) AS max_value,
  count(*)   AS n
FROM air.observations
GROUP BY 1,2,3,4;

SELECT add_continuous_aggregate_policy('air.obs_hourly',
  start_offset => INTERVAL '7 days',
  end_offset   => INTERVAL '1 hour',
  schedule_interval => INTERVAL '15 minutes');
