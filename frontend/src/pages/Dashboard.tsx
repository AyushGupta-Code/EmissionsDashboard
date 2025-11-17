import React, { useEffect, useState } from 'react';
import MapView from '../components/MapView';
import TimeSeriesPanel from '../components/TimeSeriesPanel';
import StatCards from '../components/StatCards';
import { Station, StatsSummary } from '../types';
import { getStations, getStatsSummary } from '../api/client';

export default function Dashboard(){
  const [stations, setStations] = useState<Station[]>([]);
  const [stats, setStats] = useState<StatsSummary | null>(null);

  useEffect(() => {
    getStations().then(setStations).catch(console.error);
    getStatsSummary().then(setStats).catch(console.error);
  }, []);

  const stationCountValue =
    stats?.station_count ?? (stations.length ? stations.length : undefined);

  return (
    <div className="app">
      <div className="header">
        <h3>Emissions Dashboard</h3>
        <div style={{opacity:.7}}>React • Leaflet • FastAPI • TimescaleDB</div>
      </div>
      <div className="content">
        <MapView stations={stations} />
        <div style={{display:'grid', gap:12}}>
          <StatCards stationCount={stationCountValue}
                     observationCount={stats?.observation_24h} />
          <TimeSeriesPanel />
        </div>
      </div>
    </div>
  );
}
