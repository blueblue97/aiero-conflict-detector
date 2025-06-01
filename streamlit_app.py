import streamlit as st
import pandas as pd
import geopy.distance
import folium
from streamlit_folium import folium_static

# --- UI ---
st.set_page_config(page_title="AIero Conflict Detector", layout="wide")
st.title("🧠 AIero Conflict Detector — CSV Upload")

st.write("Upload a CSV file containing aircraft data (latitude, longitude, altitude, callsign).")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Conflict detection logic
def detect_conflicts(df, threshold_km=5, threshold_alt=1000):
    conflicts = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            ac1 = df.iloc[i]
            ac2 = df.iloc[j]
            
            coords_1 = (ac1['latitude'], ac1['longitude'])
            coords_2 = (ac2['latitude'], ac2['longitude'])
            dist_km = geopy.distance.distance(coords_1, coords_2).km
            alt_diff = abs(ac1['altitude'] - ac2['altitude'])
            
            if dist_km <= threshold_km and alt_diff <= threshold_alt:
                conflicts.append({
                    'Aircraft 1': ac1['callsign'],
                    'Aircraft 2': ac2['callsign'],
                    'Distance (km)': round(dist_km, 2),
                    'Altitude Diff (ft)': int(alt_diff)
                })
    return pd.DataFrame(conflicts)

# Map display
def plot_aircraft_on_map(df):
    if df.empty:
        return
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['callsign']} (Alt: {row['altitude']})",
            icon=folium.Icon(color='blue', icon='plane', prefix='fa')
        ).add_to(m)

    folium_static(m)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {'latitude', 'longitude', 'altitude', 'callsign'}
        if not required_cols.issubset(df.columns):
            st.error(f"Missing required columns: {required_cols - set(df.columns)}")
        else:
            st.success("✅ File successfully uploaded and read!")
            st.dataframe(df)
            
            st.subheader("📍 Aircraft Map")
            plot_aircraft_on_map(df)

            st.subheader("⚠️ Detected Conflicts")
            conflicts_df = detect_conflicts(df)
            if not conflicts_df.empty:
                st.dataframe(conflicts_df)
            else:
                st.info("No conflicts detected.")
    except Exception as e:
        st.error(f"Failed to read file: {e}")
