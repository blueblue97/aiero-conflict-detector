import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# --- UI ---
st.set_page_config(page_title="AIero Conflict Detector", layout="centered")
st.title("📊 AIero — Upload Flight CSV to Detect Conflicts")

# --- Upload Section ---
uploaded_file = st.file_uploader("Upload flight data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("✈️ Raw Flight Data")
    st.dataframe(df)

    if not all(col in df.columns for col in ["flight_id", "latitude", "longitude", "altitude", "timestamp"]):
        st.error("❌ CSV must contain: flight_id, latitude, longitude, altitude, timestamp columns.")
        st.stop()

    # --- Conflict Detection ---
    st.subheader("⚠️ Detected Conflicts")

    conflicts = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            f1 = df.iloc[i]
            f2 = df.iloc[j]

            # Time check (optional: same timestamp only)
            if abs(f1["timestamp"] - f2["timestamp"]) > 10:
                continue

            # Altitude difference
            alt_diff = abs(f1["altitude"] - f2["altitude"])
            if alt_diff > 300:
                continue

            # Geo distance
            pos1 = (f1["latitude"], f1["longitude"])
            pos2 = (f2["latitude"], f2["longitude"])
            distance_km = geodesic(pos1, pos2).kilometers

            if distance_km < 10:  # < 10 km and < 300 ft = conflict
                conflicts.append({
                    "Flight 1": f1["flight_id"],
                    "Flight 2": f2["flight_id"],
                    "Alt Diff (ft)": alt_diff,
                    "Distance (km)": round(distance_km, 2),
                    "Time 1": f1["timestamp"],
                    "Time 2": f2["timestamp"]
                })

    if conflicts:
        conflict_df = pd.DataFrame(conflicts)
        st.success(f"✅ {len(conflicts)} conflicts found!")
        st.dataframe(conflict_df)
    else:
        st.info("No conflicts found ✅")
