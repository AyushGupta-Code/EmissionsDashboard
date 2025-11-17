import React from 'react';

type Stat = { label: string; value: string | number; };

export default function StatCards(){
  const stats: Stat[] = [
    { label: 'Stations', value: '—' },
    { label: 'Observations (24h)', value: '—' },
    { label: 'Parameters', value: 'pm25, pm10, o3, no2' },
  ];
  return (
    <div className="card" style={{display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:12}}>
      {stats.map((s,i)=> (
        <div key={i} style={{padding:'8px 12px'}}>
          <div style={{fontSize:12, color:'#666'}}>{s.label}</div>
          <div style={{fontSize:22, fontWeight:700}}>{s.value}</div>
        </div>
      ))}
    </div>
  )
}
