import streamlit as st
import json
import requests
from opensky_fetch import fetch_opensky_data
from sky_brain import detect_conflicts, visualize_conflicts_on_map

# Load credentials
with open("credentials.json") as file:
    creds = json.load(file)
    client_id = creds["client_id"]
    client_secret = creds["client_secret"]

# Title
st.set_page_config(page_title="AIero Conflict Detector")
st.title("🧠 Sky Brain — Conflict Detection System")

# Live data
data = fetch_opensky_data(client_id, client_secret)

if data:
    st.success("✅ Live data received!")
    st.json(data)

    # Map visualization
    map_component = visualize_conflicts_on_map(data)
    if map_component:
        st.subheader("✈️ Aircraft Map")
        st.pydeck_chart(map_component)

    # Run Sky Brain analysis
    conflicts = detect_conflicts(data)

    if conflicts:
        st.warning("⚠️ Potential Conflicts Detected")
        for conflict in conflicts:
            st.write(conflict)
    else:
        st.info("✅ No conflicts detected")
else:
    st.error("❌ Failed to retrieve data from OpenSky API")
