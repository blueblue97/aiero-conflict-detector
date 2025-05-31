
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import streamlit as st

# UI
st.title("🌍 Live Aircraft Data Viewer (OpenSky)")
st.write("Real-time flight data from OpenSky Network")

username = st.text_input("Enter OpenSky Username")
password = st.text_input("Enter OpenSky Password", type="password")

if username and password:
    with st.spinner("Fetching data..."):
        url = "https://opensky-network.org/api/states/all"

        try:
            response = requests.get(url, auth=HTTPBasicAuth(username, password))
            data = response.json()

            if data and "states" in data:
                df = pd.DataFrame(data["states"], columns=[
                    "icao24", "callsign", "origin_country", "time_position", "last_contact",
                    "longitude", "latitude", "baro_altitude", "on_ground", "velocity", "heading",
                    "vertical_rate", "sensors", "geo_altitude", "squawk", "spi", "position_source"
                ])
                st.dataframe(df[["icao24", "callsign", "origin_country", "latitude", "longitude", "velocity"]])
            else:
                st.error("No data returned.")
        except Exception as e:
            st.error(f"Error: {e}")
