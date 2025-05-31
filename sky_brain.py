import pandas as pd
import pydeck as pdk

def visualize_conflicts_on_map(data):
    if not data or "states" not in data or not data["states"]:
        return None

    columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "heading", "vertical_rate", "sensors", "geo_altitude", "squawk",
        "spi", "position_source"
    ]

    df = pd.DataFrame(data["states"], columns=columns)
    df = df.dropna(subset=["latitude", "longitude", "geo_altitude"])

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=500,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=4,
        pitch=40
    )

    return pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Altitude: {geo_altitude}\nVelocity: {velocity}\nCountry: {origin_country}"}
    )
