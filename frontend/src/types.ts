export type Station = {
  station_id: string;
  name?: string;
  provider?: string;
  country?: string;
  city?: string;
  latitude: number;
  longitude: number;
};

export type Observation = {
  time: string;
  station_id: string;
  parameter: string;
  unit: string;
  value: number;
  quality?: string;
  source?: string;
};

export type StatsSummary = {
  station_count: number;
  observation_24h: number;
};
