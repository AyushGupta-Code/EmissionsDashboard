INSERT INTO air.stations (station_id, name, provider, country, city, latitude, longitude, first_seen)
VALUES
('DEMO_1','Demo Station 1','demo','US','Raleigh',35.7796,-78.6382, now())
ON CONFLICT DO NOTHING;

INSERT INTO air.observations (time, station_id, parameter, unit, value, quality, source)
VALUES
(now() - interval '2 hours','DEMO_1','pm25','µg/m³',14.2,'ok','demo'),
(now() - interval '1 hours','DEMO_1','pm25','µg/m³',18.9,'ok','demo'),
(now(),                   'DEMO_1','pm25','µg/m³',12.1,'ok','demo')
ON CONFLICT DO NOTHING;
