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

# Set page title and layout
st.set_page_config(page_title="🛫 AIero Sky Brain", layout="wide")
st.title("🧠 Sky Brain – Live Conflict Detection Dashboard")

# Fetch live OpenSky data
data = fetch_opensky_data(client_id, client_secret)

if data:
    st.success("✅ Live data received!")
    
    # Display raw JSON
    with st.expander("📦 Raw JSON Data"):
        st.json(data)

    # Detect conflicts using AI logic
    conflicts = detect_conflicts(data)

    # Display map
    st.subheader("🗺️ Aircraft Map")
    
    states = data.get("states", [])
    aircraft_data = [
        {
            "icao24": s[0],
            "callsign": s[1].strip() if s[1] else "",
            "origin_country": s[2],
            "longitude": s[5],
            "latitude": s[6],
            "altitude": s[7]
        }
        for s in states if s[5] is not None and s[6] is not None
    ]

    df = pd.DataFrame(aircraft_data)

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=37.7749,
            longitude=-95,
            zoom=3,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[longitude, latitude]',
                get_color='[0, 0, 255, 160]',
                get_radius=30000,
            ),
        ],
    ))

    # Display conflict alerts
    if conflicts:
        st.subheader("🚨 Potential Conflicts Detected")
        for conflict in conflicts:
            st.error(conflict)
    else:
        st.success("✅ No immediate conflicts detected.")
else:
    st.error("❌ Failed to load live data from OpenSky.")
