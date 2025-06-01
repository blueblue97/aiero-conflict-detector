import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from sky_brain import detect_conflicts

# UI Setup
st.set_page_config(page_title="AIero Conflict Detector")
st.title("🧠 Sky Brain — Upload Conflict Detection")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file with aircraft data", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.write("### Data Preview:")
    st.dataframe(df)

    # Detect conflicts
    conflicts = detect_conflicts(df)

    if conflicts:
        st.warning("⚠️ Potential Conflicts Detected:")
        for conflict in conflicts:
            st.write(conflict)

        # Show map
        m = folium.Map(location=[conflicts[0]['lat1'], conflicts[0]['lon1']], zoom_start=6)
        for conflict in conflicts:
            folium.Marker(location=[conflict['lat1'], conflict['lon1']], tooltip="Aircraft 1").add_to(m)
            folium.Marker(location=[conflict['lat2'], conflict['lon2']], tooltip="Aircraft 2").add_to(m)
        st.write("### Conflict Locations Map")
        folium_static(m)
    else:
        st.success("✅ No conflicts detected in the uploaded data.")

else:
    st.info("📂 Please upload a CSV file to begin analysis.")
