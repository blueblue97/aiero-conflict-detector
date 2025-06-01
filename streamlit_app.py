
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from opensky_api import OpenSkyApi
from datetime import datetime

# Function to detect conflicts from CSV
def detect_conflicts(df):
    conflicts = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            same_time = df.iloc[i]["time"] == df.iloc[j]["time"]
            close_lat = abs(df.iloc[i]["lat"] - df.iloc[j]["lat"]) < 0.1
            close_lon = abs(df.iloc[i]["lon"] - df.iloc[j]["lon"]) < 0.1
            close_alt = abs(df.iloc[i]["altitude"] - df.iloc[j]["altitude"]) < 1000
            if same_time and close_lat and close_lon and close_alt:
                conflicts.append((i, j))
    return conflicts

# Title
st.title("🛫 AIero Conflict Detector: CSV Upload + Real-Time OpenSky Overlay")

# Upload CSV
uploaded_file = st.file_uploader("Upload Flight CSV", type="csv")

# Initialize Folium map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="cartodbpositron")

# Plot real-time OpenSky data
try:
    api = OpenSkyApi()
    states = api.get_states()
    if states and states.states:
        for s in states.states:
            if s.latitude is not None and s.longitude is not None:
                popup = f"Callsign: {s.callsign.strip()}<br>Altitude: {s.baro_altitude} m"
                folium.CircleMarker(
                    location=[s.latitude, s.longitude],
                    radius=4,
                    color="blue",
                    fill=True,
                    fill_opacity=0.7,
                    popup=popup,
                ).add_to(m)
except Exception as e:
    st.warning(f"Could not fetch OpenSky data: {e}")

# If CSV uploaded
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "lat" in df.columns and "lon" in df.columns:
        st.success("CSV loaded successfully.")
        conflicts = detect_conflicts(df)

        # Plot conflicting flights
        for i, j in conflicts:
            for idx in (i, j):
                row = df.iloc[idx]
                popup = f"Flight: {row['flight_id']}<br>Altitude: {row['altitude']}<br>Time: {row['time']}"
                folium.Marker(
                    location=[row["lat"], row["lon"]],
                    popup=popup,
                    icon=folium.Icon(color="red", icon="exclamation-sign"),
                ).add_to(m)

# Display map
st_folium(m, width=1000, height=600)
