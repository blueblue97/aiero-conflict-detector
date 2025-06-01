import streamlit as st
import json
import requests
import pydeck as pdk
from opensky_fetch import fetch_opensky_data
from sky_brain import detect_conflicts

# Load credentials
with open("credentials.json") as file:
    creds = json.load(file)
client_id = creds["client_id"]
client_secret = creds["client_secret"]

st.set_page_config(page_title="AIero Conflict Detector", layout="wide")
st.title("🌐 AIero – Live Aircraft Conflict Detection")

# Fetch OpenSky data
data = fetch_opensky_data(client_id, client_secret)

if data:
    st.success("✅ Live data received!")

    states = data.get("states", [])
    columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "true_track", "vertical_rate", "sensors", "geo_altitude",
        "squawk", "spi", "position_source"
    ]
    df = [dict(zip(columns, s)) for s in states if s[5] is not None and s[6] is not None]

    st.subheader("📍 Aircraft Map")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=39.8283,
            longitude=-98.5795,
            zoom=3,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position="[longitude, latitude]",
                get_color="[200, 30, 0, 160]",
                get_radius=30000,
                pickable=True,
            ),
        ],
        tooltip={"text": "Callsign: {callsign}\nAltitude: {baro_altitude}"}
    ))

    st.subheader("⚠️ Detected Conflicts")
    conflicts = detect_conflicts(data)
    if conflicts:
        for conflict in conflicts:
            st.warning(f"Potential conflict: {conflict}")
    else:
        st.info("No conflicts detected.")
else:
    st.error("❌ Failed to fetch data from OpenSky.")
