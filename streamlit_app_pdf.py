
# streamlit_app_pdf.py
import streamlit as st
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import pydeck as pdk
from fpdf import FPDF
import tempfile
import os

def detect_conflicts(df, horizontal_sep_nm=5, vertical_sep_ft=1000):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)
    conflicts = []

    for time_point in df['timestamp'].unique():
        snapshot = df[df['timestamp'] == time_point]
        aircrafts = snapshot.to_dict('records')

        for i in range(len(aircrafts)):
            for j in range(i + 1, len(aircrafts)):
                a1 = aircrafts[i]
                a2 = aircrafts[j]

                dist_nm = geodesic((a1['latitude'], a1['longitude']), (a2['latitude'], a2['longitude'])).nautical
                alt_diff = abs(a1['altitude_ft'] - a2['altitude_ft'])

                if dist_nm < horizontal_sep_nm and alt_diff < vertical_sep_ft:
                    conflicts.append({
                        "timestamp": time_point,
                        "aircraft_1": a1['aircraft_id'],
                        "aircraft_2": a2['aircraft_id'],
                        "distance_nm": round(dist_nm, 2),
                        "altitude_diff_ft": alt_diff
                    })
    return pd.DataFrame(conflicts)

def generate_conflict_pdf(dataframe, logo_path="aiero_logo.png"):
    pdf = FPDF()
    pdf.add_page()

    try:
        pdf.image(logo_path, x=10, y=8, w=40)
    except:
        pass

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AIero | Air Traffic Conflict Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)

    col_widths = [40, 40, 40, 35, 35]
    headers = ["Timestamp", "Aircraft 1", "Aircraft 2", "Distance (NM)", "Altitude Diff (ft)"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align='C')
    pdf.ln()

    for _, row in dataframe.iterrows():
        pdf.cell(col_widths[0], 8, str(row["timestamp"]), border=1)
        pdf.cell(col_widths[1], 8, row["aircraft_1"], border=1)
        pdf.cell(col_widths[2], 8, row["aircraft_2"], border=1)
        pdf.cell(col_widths[3], 8, str(row["distance_nm"]), border=1)
        pdf.cell(col_widths[4], 8, str(row["altitude_diff_ft"]), border=1)
        pdf.ln()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

def main():
    st.set_page_config(
        page_title="AIero | Conflict Detector",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.sidebar.image("aiero_logo.png", use_container_width=True)
    st.sidebar.markdown("### AIero Airspace Intelligence")
    st.sidebar.markdown("Built for mission-critical airspace safety.")

    st.title("✈️ AIero | Air Traffic Conflict Detector")

    uploaded_file = st.file_uploader("📤 Upload Flight Data CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.subheader("📊 Flight Data Preview")
        st.dataframe(df.head())

        st.subheader("🗺 Aircraft Map View + Altitude Coloring")
        latest = df[df['timestamp'] == df['timestamp'].max()]
        min_alt = df['altitude_ft'].min()
        max_alt = df['altitude_ft'].max()

        def get_altitude_color(alt):
            scale = int(((alt - min_alt) / (max_alt - min_alt)) * 255)
            return [scale, 255 - scale, 150]

        latest['color'] = latest['altitude_ft'].apply(get_altitude_color)

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v10',
            initial_view_state=pdk.ViewState(
                latitude=latest['latitude'].mean(),
                longitude=latest['longitude'].mean(),
                zoom=6,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=latest,
                    get_position='[longitude, latitude]',
                    get_color='color',
                    get_radius=1200,
                ),
                pdk.Layer(
                    "TextLayer",
                    data=latest,
                    get_position='[longitude, latitude]',
                    get_text='aircraft_id',
                    get_size=16,
                    get_color=[255, 255, 255],
                    get_angle=0,
                    get_alignment_baseline="'bottom'"
                )
            ],
        ))

        st.subheader("⚠️ Detected Conflicts")
        conflicts_df = detect_conflicts(df)
        st.dataframe(conflicts_df)

        if not conflicts_df.empty:
            csv = conflicts_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Conflict Report (CSV)", csv, "conflict_report.csv", "text/csv")

            pdf_path = generate_conflict_pdf(conflicts_df)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download Conflict Report (PDF)", f, "conflict_report.pdf", "application/pdf")

if __name__ == "__main__":
    main()
