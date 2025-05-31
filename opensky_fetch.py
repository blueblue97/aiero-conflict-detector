import streamlit as st
import requests
import json

# Load credentials
with open("credentials.json", "r") as f:
    creds = json.load(f)

client_id = creds["client_id"]
client_secret = creds["client_secret"]

# Get access token
auth_response = requests.post(
    "https://login.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token",
    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
)

if auth_response.status_code != 200:
    st.error("Auth failed: " + auth_response.text)
    st.stop()

access_token = auth_response.json()["access_token"]

# Fetch OpenSky data
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get("https://opensky-network.org/api/states/all", headers=headers)

st.title("Live Aircraft Data Viewer (OpenSky)")

if response.status_code == 200:
    data = response.json()
    st.write(data)
else:
    st.error("Failed to fetch data: " + response.text)
