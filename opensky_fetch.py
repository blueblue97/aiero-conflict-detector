import pandas as pd
from opensky_api import OpenSkyApi

def fetch_opensky_data():
    api = OpenSkyApi()
    states = api.get_states()
    flights = []
    if states and states.states:
        for s in states.states:
            if s.latitude is not None and s.longitude is not None:
                flights.append({
                    "icao24": s.icao24,
                    "callsign": s.callsign.strip() if s.callsign else "N/A",
                    "origin_country": s.origin_country,
                    "longitude": s.longitude,
                    "latitude": s.latitude,
                    "altitude": s.baro_altitude or 0,
                })
    return pd.DataFrame(flights)
