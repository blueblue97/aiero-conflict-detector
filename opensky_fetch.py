import streamlit as st
import requests
import json

# Load OpenSky credentials
with open("credentials.json", "r") as f:
    credentials = json.load(f)

client_id = credentials["client_id"]
client_secret = credentials["client_secret"]

# Get access token from OpenSky
def get_access_token():
    token_url = "https://login.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, data=payload)
    return response.json().get("access_token")

# Call OpenSky with access token
def fetch_data():
    token = get_access_token()
    if not token:
        st.error("Failed to get token.")
        return
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get("https://opensky-network.org/api/states/all", headers=headers)
    if r.status_code == 200:
        data = r.json()
        st.success("Data retrieved!")
        st.json(data)
    else:
        st.error("Failed to fetch data.")

# Streamlit UI
st.title("Live Aircraft Data Viewer")
if st.button("Fetch Live Data"):
    fetch_data()
