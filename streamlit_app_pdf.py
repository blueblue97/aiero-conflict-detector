import streamlit as st
import json
import requests
from opensky_fetch import fetch_opensky_data
from sky_brain import detect_conflicts

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

    # Run Sky Brain analysis
    conflicts = detect_conflicts(data)

    if conflicts:
        st.error("⚠️ Potential Conflicts Detected:")
        for c in conflicts:
            st.write(f"- Between {c['callsign_1']} and {c['callsign_2']}, "
                     f"Separation: {c['distance_km']:.2f} km")
    else:
        st.success("✅ No immediate conflicts detected.")
else:
    st.error("❌ Could not fetch live aircraft data.")
