import streamlit as st
import requests
import json

# Load credentials
with open("credentials.json") as file:
    creds = json.load(file)

client_id = creds["client_id"]
client_secret = creds["client_secret"]

# Get access token
auth_url = "https://login.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
auth_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

auth_response = requests.post(auth_url, data=auth_data)
if auth_response.status_code != 200:
    st.error("❌ Failed to get access token.")
    st.stop()

access_token = auth_response.json()["access_token"]

# Get live state vector data from OpenSky
headers = {"Authorization": f"Bearer {access_token}"}
data_url = "https://opensky-network.org/api/states/all"
response = requests.get(data_url, headers=headers)

# Display results
st.title("🌍 Live Aircraft Data Viewer (OpenSky API)")
if response.status_code == 200:
    data = response.json()
    st.success("✅ Live aircraft data retrieved!")
    st.write(data)
else:
    st.error("❌ Failed to retrieve aircraft data.")
