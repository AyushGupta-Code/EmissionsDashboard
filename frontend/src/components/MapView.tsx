import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { Station } from '../types';
import { getStations } from '../api/client';

const icon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconSize: [25,41], iconAnchor: [12,41]
});

export default function MapView(){
  const [stations, setStations] = useState<Station[]>([]);
  useEffect(()=>{ getStations().then(setStations).catch(console.error); },[]);

  return (
    <div className="card map">
      <MapContainer center={[35.7796, -78.6382]} zoom={6} style={{height:'100%'}}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {stations.map(s => (
          <Marker key={s.station_id} position={[s.latitude, s.longitude]} icon={icon}>
            <Popup>
              <b>{s.name || s.station_id}</b><br/>
              {(s.city || '')} {(s.country || '')}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
