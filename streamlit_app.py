import streamlit as st
import pandas as pd
from io import StringIO

# Function to detect conflicts in flight data
def detect_conflicts(df):
    conflicts = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            same_time = df.iloc[i]["time"] == df.iloc[j]["time"]
            close_lat = abs(df.iloc[i]["latitude"] - df.iloc[j]["latitude"]) < 0.1
            close_lon = abs(df.iloc[i]["longitude"] - df.iloc[j]["longitude"]) < 0.1
            close_alt = abs(df.iloc[i]["altitude"] - df.iloc[j]["altitude"]) < 1000
            if same_time and close_lat and close_lon and close_alt:
                conflicts.append((i, j))
    return conflicts

st.set_page_config(page_title="CSV Conflict Detector")
st.title("📄 Upload CSV for Conflict Detection")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Flight Data")
    st.dataframe(df)

    conflicts = detect_conflicts(df)
    if conflicts:
        st.error(f"⚠️ {len(conflicts)} potential conflict(s) detected!")
        for c in conflicts:
            st.write(f"Conflict between flight {c[0]} and flight {c[1]}")
    else:
        st.success("✅ No conflicts detected.")