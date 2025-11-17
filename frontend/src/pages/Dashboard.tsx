import React from 'react';
import MapView from '../components/MapView';
import TimeSeriesPanel from '../components/TimeSeriesPanel';
import StatCards from '../components/StatCards';

export default function Dashboard(){
  return (
    <div className="app">
      <div className="header">
        <h3>Emissions Dashboard</h3>
        <div style={{opacity:.7}}>React • Leaflet • FastAPI • TimescaleDB</div>
      </div>
      <div className="content">
        <MapView />
        <div style={{display:'grid', gap:12}}>
          <StatCards />
          <TimeSeriesPanel />
        </div>
      </div>
    </div>
  );
}
