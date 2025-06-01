import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import MarkerCluster

# --- UI ---
st.set_page_config(page_title="AIero Conflict Detector", layout="wide")
st.title("✈️ AIero Conflict Detector")
st.markdown("Upload a CSV with flight data. If there are conflicts, you'll see them below and on the interactive map.")

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload flight CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Flight Data")
    st.dataframe(df)

    # --- Conflict Detection ---
    def detect_conflicts(data):
        conflicts = []
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                same_time = data.iloc[i]["time"] == data.iloc[j]["time"]
                close_lat = abs(data.iloc[i]["latitude"] - data.iloc[j]["latitude"]) < 1.0
                close_lon = abs(data.iloc[i]["longitude"] - data.iloc[j]["longitude"]) < 1.0
                close_alt = abs(data.iloc[i]["altitude"] - data.iloc[j]["altitude"]) < 1000

                if same_time and close_lat and close_lon and close_alt:
                    conflicts.append({
                        "flight_id": data.iloc[i]["flight_id"],
                        "time": data.iloc[i]["time"],
                        "latitude": data.iloc[i]["latitude"],
                        "longitude": data.iloc[i]["longitude"],
                        "altitude": data.iloc[i]["altitude"],
                        "conflict_type": "Potential Conflict"
                    })
        return pd.DataFrame(conflicts)

    conflicts = detect_conflicts(df)

    if not conflicts.empty:
        st.subheader("⚠️ Detected Conflicts")
        st.dataframe(conflicts)

        # --- Folium Map ---
        st.subheader("🗺️ Conflict Map")
        m = folium.Map(location=[20, 0], zoom_start=2)
        cluster = MarkerCluster().add_to(m)

        for _, row in conflicts.iterrows():
            popup = f"""
            <b>Flight:</b> {row['flight_id']}<br>
            <b>Time:</b> {row['time']}<br>
            <b>Altitude:</b> {row['altitude']} ft<br>
            <b>Type:</b> {row['conflict_type']}
            """
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=6,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.7,
                popup=popup,
            ).add_to(cluster)

        m.save("/tmp/map.html")
        components.html(open("/tmp/map.html", "r").read(), height=600)
    else:
        st.success("✅ No conflicts detected.")
else:
    st.info("Upload a CSV file to begin.")
