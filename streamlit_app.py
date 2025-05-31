import streamlit as st
import json
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

from opensky_fetch import fetch_opensky_data
from sky_brain import detect_conflicts

# Load credentials
with open("credentials.json") as file:
    creds = json.load(file)
client_id = creds["client_id"]
client_secret = creds["client_secret"]

# Title
st.set_page_config(page_title="AIero Conflict Detector", layout="wide")
st.title("🛰️ Sky Brain — Conflict Detection System")

# Live data
data = fetch_opensky_data(client_id, client_secret)

if data:
    st.success("✅ Live data received!")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("📄 Raw JSON Data")
        st.json(data)

    with col2:
        st.subheader("🗺️ Aircraft Positions Map")
        m = folium.Map(location=[20, 0], zoom_start=2)

        for state in data.get("states", []):
            try:
                lat = state[6]
                lon = state[5]
                callsign = state[1].strip() if state[1] else "N/A"
                if lat is not None and lon is not None:
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"Callsign: {callsign}",
                        icon=folium.Icon(color="blue", icon="plane", prefix="fa")
                    ).add_to(m)
            except Exception:
                continue

        st_data = st_folium(m, width=700, height=500)

    # Conflict detection
    conflicts = detect_conflicts(data)
    if conflicts:
        st.warning("⚠️ Potential conflicts detected!")
        for conflict in conflicts:
            st.write(conflict)
    else:
        st.info("✅ No conflicts detected.")
else:
    st.error("❌ Failed to fetch data from OpenSky.")
