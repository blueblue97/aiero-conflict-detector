import streamlit as st
import requests
import json

# Load OpenSky credentials
with open("credentials.json", "r") as file:
    creds = json.load(file)

client_id = creds["clientId"]
client_secret = creds["clientSecret"]

# Get access token using client credentials flow
def get_token():
    url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token", None)

# Fetch live state vectors (aircraft data)
def fetch_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://opensky-network.org/api/states/all", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Streamlit app UI
st.title("🌍 Live Aircraft Data Viewer (OpenSky API)")

token = get_token()
if token:
    data = fetch_data(token)
    if data:
        st.success("✅ Live data received!")
        st.json(data)
    else:
        st.warning("⚠️ No aircraft data returned.")
else:
    st.error("❌ Failed to get access token.")
