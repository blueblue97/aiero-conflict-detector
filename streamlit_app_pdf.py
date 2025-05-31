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

# Page Setup
st.set_page_config(page_title="AIero Conflict Detector", layout="wide")
st.title("✈️ AIero Sky Brain — Live Conflict Detection System")

# Get Data
data = fetch_opensky_data(client_id, client_secret)

if not data:
    st.error("⚠️ No data received from OpenSky.")
    st.stop()
else:
    st.success("✅ Live data received!")
    states = data.get("states", [])

# Conflict Detection
conflicts = detect_conflicts(data)

# Conflict Map
if states:
    aircraft_df = []
    for s in states:
        if s[5] is not None and s[6] is not None and s[13] is not None:
            aircraft_df.append({
                "icao24": s[0],
                "callsign": s[1].strip() if s[1] else "",
                "origin_country": s[2],
                "longitude": s[5],
                "latitude": s[6],
                "altitude": s[13]
            })

    # Display Map
    st.subheader("🗺️ Aircraft Positions (Real-time)")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1,
            pitch=45,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=aircraft_df,
                get_position='[longitude, latitude]',
                get_color='[0, 150, 255, 180]',
                get_radius=40000,
            )
        ],
    ))

# Conflict Section
if conflicts:
    st.subheader("🚨 Potential Conflicts Detected")
    for c in conflicts:
        st.markdown(f"- **{c['callsign_1']}** vs **{c['callsign_2']}** — Distance: `{c['distance_km']} km`, Alt Diff: `{c['altitude_diff']} m`")
else:
    st.info("✅ No immediate conflicts detected.")
