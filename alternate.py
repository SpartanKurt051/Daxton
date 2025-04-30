import streamlit as st
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    'City': ['New York', 'London', 'Tokyo', 'Sydney'],
    'lat': [40.7128, 51.5074, 35.6895, -33.8688],
    'lon': [-74.0060, -0.1278, 139.6917, 151.2093],
    'value': [100, 200, 300, 400]
})

# Projection type selector
projection = st.selectbox("Choose a map projection:", [
    "equirectangular", "orthographic", "natural earth",
    "kavrayskiy7", "mercator", "miller", "robinson", "mollweide", 
    "azimuthal equal area", "azimuthal equidistant", "conic equal area", 
    "conic conformal", "conic equidistant", "gnomonic", "stereographic", 
    "transverse mercator", "winkel tripel", "aitoff", "hammer", "sinusoidal"
])

# Plotly scatter_geo
fig = px.scatter_geo(
    df,
    lat='lat',
    lon='lon',
    text='City',
    size='value',
    projection=projection
)

fig.update_geos(showcoastlines=True, showland=True, fitbounds="locations")

st.plotly_chart(fig)
