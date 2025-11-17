import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import { getHourly } from '../api/client';

export default function TimeSeriesPanel(){
  const [data, setData] = useState<any[]>([]);
  const [station, setStation] = useState('DEMO_1');
  const [param, setParam] = useState('pm25');

  useEffect(()=>{
    getHourly({station_id: station, parameter: param}).then(setData).catch(console.error)
  },[station, param]);

  return (
    <div className="card chart">
      <div className="controls">
        <label>Station</label>
        <input value={station} onChange={e=>setStation(e.target.value)} />
        <label>Parameter</label>
        <select value={param} onChange={e=>setParam(e.target.value)}>
          <option value="pm25">pm25</option>
          <option value="pm10">pm10</option>
          <option value="no2">no2</option>
          <option value="o3">o3</option>
        </select>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ left: 12, right: 12, top: 12, bottom: 12 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" tickFormatter={(v)=> new Date(v).toLocaleString()} minTickGap={32} />
          <YAxis />
          <Tooltip labelFormatter={(v)=> new Date(v as string).toLocaleString()} />
          <Line type="monotone" dataKey="avg_value" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
