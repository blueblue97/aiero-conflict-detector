import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from opensky_fetch import fetch_opensky_data
from sky_brain import detect_conflicts

st.set_page_config(page_title="Aiero Conflict Detector", layout="wide")
st.title("🧠 Aiero Conflict Detector — CSV & Real-Time Airspace")

uploaded_file = st.file_uploader("Upload CSV with flight data", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Flight Data")
    st.dataframe(df)

    conflicts = detect_conflicts(df)
    if conflicts:
        st.warning("⚠️ Conflicts detected!")
    else:
        st.success("✅ No conflicts detected.")

    conflict_df = pd.DataFrame(conflicts)
    if not conflict_df.empty:
        st.subheader("🗺️ Conflict Map (CSV + Real-Time)")
        m = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodb dark_matter")

        for row in conflict_df.itertuples():
            folium.Marker(
                location=[row.latitude, row.longitude],
                popup=f"{row.flight_id} | Alt: {row.altitude}",
                icon=folium.Icon(color="red")
            ).add_to(m)

        opensky_df = fetch_opensky_data()
        for row in opensky_df.itertuples():
            folium.CircleMarker(
                location=[row.latitude, row.longitude],
                radius=4,
                popup=f"{row.callsign}",
                color="blue",
                fill=True,
                fill_opacity=0.4
            ).add_to(m)

        st_folium(m, height=600)
