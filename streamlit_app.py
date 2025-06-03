import streamlit as st
from opensky_api import OpenSkyApi
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

api = OpenSkyApi()

st.title("🛫 Flight Conflict Detector by Flight Number")

flight_number = st.text_input("Enter Flight Number (e.g., TP344)")

if flight_number:
    st.write(f"Searching for flight: **{flight_number.upper()}**")

    # Get all states
    states = api.get_states()

    target = None
    for s in states.states:
        if s.callsign and flight_number.upper() in s.callsign.strip():
            target = s
            break

    if target:
        st.success(f"Found flight {target.callsign.strip()}")

        lat, lon = target.latitude, target.longitude
        alt = target.baro_altitude

        st.write(f"Location: ({lat}, {lon}) at {alt} m")

        # Map setup
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], tooltip=f"{target.callsign.strip()} (Target)", icon=folium.Icon(color='red')).add_to(m)

        # Search nearby flights
        conflict_flights = []
        for s in states.states:
            if s != target and s.latitude and s.longitude:
                dist = geodesic((lat, lon), (s.latitude, s.longitude)).km
                if dist < 100:  # within 100 km
                    alt_diff = abs((s.baro_altitude or 0) - (alt or 0))
                    if alt_diff < 300:  # less than 300m vertical difference
                        conflict_flights.append((s, dist, alt_diff))
                        folium.Marker(
                            [s.latitude, s.longitude],
                            tooltip=f"{s.callsign.strip()} | Alt Diff: {alt_diff:.0f}m | {dist:.1f}km",
                            icon=folium.Icon(color='orange')
                        ).add_to(m)

        st_folium(m, width=700)

        st.subheader("⚠️ Potential Conflicts")
        if conflict_flights:
            for c, d, a in conflict_flights:
                st.write(f"- {c.callsign.strip()} at ({c.latitude}, {c.longitude}) | Dist: {d:.1f} km | Alt Diff: {a:.0f} m")
        else:
            st.success("No nearby conflicts detected.")

    else:
        st.error("Flight not found.")
