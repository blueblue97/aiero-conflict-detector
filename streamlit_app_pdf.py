import streamlit as st
import json
import requests
import pandas as pd
import pydeck as pdk
from opensky_fetch import fetch_opensky_data
from sky_brain import detect_conflicts

# Load credentials
with open("credentials.json") as file:
    creds = json.load(file)
client_id = creds["client_id"]
client_secret = creds["client_secret"]

# Set page
st.set_page_config(page_title="AIero Sky Brain", layout="wide")
st.title("🧠 Sky Brain – Live Air Conflict Detection System")

# Fetch live data
data = fetch_opensky_data(client_id, client_secret)

if data:
    st.success("✅ Live data received!")

    # Show raw JSON
    with st.expander("📦 Raw Aircraft Data"):
        st.json(data)

    # Run conflict detection
    conflicts = detect_conflicts(data)

    if conflicts:
        st.error(f"⚠️ {len(conflicts)} Potential Conflict(s) Detected")
        for conflict in conflicts:
            st.write(conflict)
    else:
        st.success("✅ No conflicts found.")

    # Visualize on map
    st.subheader("🌍 Aircraft Positions")
    states = data.get("states", [])
    df = pd.DataFrame(states, columns=[
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity", "true_track",
        "vertical_rate", "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ])

    # Remove empty entries
    df = df.dropna(subset=["longitude", "latitude"])

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df["latitude"].mean(),
            longitude=df["longitude"].mean(),
            zoom=3,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=40000,
                pickable=True,
            )
        ],
        tooltip={"text": "Callsign: {callsign}\nCountry: {origin_country}\nAltitude: {baro_altitude}"}
    ))

else:
    st.error("❌ Failed to retrieve aircraft data.")
