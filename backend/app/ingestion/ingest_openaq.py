import os, sys, httpx
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
OPENAQ_BASE_URL = os.getenv("OPENAQ_BASE_URL", "https://api.openaq.org/v2")

since = "2025-01-01"
if "--since" in sys.argv:
    since = sys.argv[sys.argv.index("--since") + 1]

def upsert_station(conn, s):
    sql = text(
        """
        INSERT INTO air.stations (station_id, name, provider, country, city, latitude, longitude, first_seen, last_seen)
        VALUES (:id, :name, 'openaq', :country, :city, :lat, :lon, now(), now())
        ON CONFLICT (station_id) DO UPDATE SET name=EXCLUDED.name, country=EXCLUDED.country, city=EXCLUDED.city, latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude, last_seen=now();
        """
    )
    conn.execute(sql, {
        "id": str(s["id"]),
        "name": s.get("name"),
        "country": s.get("country"),
        "city": s.get("city"),
        "lat": s["coordinates"]["latitude"],
        "lon": s["coordinates"]["longitude"],
    })

def insert_observations(conn, measurements):
    sql = text(
        """
        INSERT INTO air.observations (time, station_id, parameter, unit, value, quality, source)
        VALUES (:time, :station_id, :parameter, :unit, :value, :quality, 'openaq')
        ON CONFLICT DO NOTHING
        """
    )
    conn.execute(sql, measurements)

def fetch_and_load():
    with engine.begin() as conn:
        page = 1
        while True:
            params = {
                "limit": 100,
                "page": page,
                "date_from": since,
                "order_by": "datetime",
                "sort": "asc",
            }
            r = httpx.get(f"{OPENAQ_BASE_URL}/measurements", params=params, timeout=60)
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])
            if not results:
                break

            stations = {}
            measurements = []
            for rec in results:
                loc = rec.get("locationId") or rec.get("location")
                if isinstance(loc, dict):
                    sid = loc.get("id")
                    coords = loc.get("coordinates", {})
                    station = {
                        "id": sid,
                        "name": loc.get("name"),
                        "country": loc.get("country"),
                        "city": loc.get("city"),
                        "coordinates": {"latitude": coords.get("latitude"), "longitude": coords.get("longitude")}
                    }
                else:
                    sid = str(loc)
                    station = {"id": sid, "name": f"OpenAQ {sid}", "country": None, "city": None, "coordinates": {"latitude": rec["coordinates"]["latitude"], "longitude": rec["coordinates"]["longitude"]}}
                stations[str(sid)] = station

                measurements.append({
                    "time": rec["date"]["utc"],
                    "station_id": str(station["id"]),
                    "parameter": rec["parameter"],
                    "unit": rec.get("unit", "unknown"),
                    "value": rec["value"],
                    "quality": rec.get("validation", {}).get("status"),
                })

            for s in stations.values():
                upsert_station(conn, s)
            if measurements:
                insert_observations(conn, measurements)

            page += 1

if __name__ == "__main__":
    fetch_and_load()
    print("✅ OpenAQ ingestion complete")
