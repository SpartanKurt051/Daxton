import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit App
st.title("Geospatial Distribution of Employees")

# Data provided by user along with latitude and longitude
location_data = pd.DataFrame({
    "Location": [
        "Trichy", "Miami", "Mumbai", "Ohio", "Kingston", "Chennai", "Vijayawada", "Liverpool",
        "Atlanta", "Laporte", "Pontypridd", "Palm Bay", "Hyderabad", "Thousand Oaks",
        "Southampton", "Taguig", "Colorado Springs", "Banbury", "Middlesbrough",
        "Derby", "Dallas", "Birmingham", "Louisville", "Derry", "Bangalore",
        "Chico", "Fort Worth", "Belfast", "Amherst", "Cebu", "Gurugram",
        "Salt Lake City", "Edinburgh", "Manchester", "Chattanooga", "Tampa", "Rockford",
        "Mexico City", "Puducherry", "Fortscott", "Columbus", "Belleville", "Melbourne"
    ],
    "Count": [
        447, 5, 6489, 69, 77, 2834, 167, 33,
        19, 41, 581, 233, 2366, 115,
        2, 1147, 421, 33, 399,
        477, 540, 154, 832, 255, 3625,
        2, 1, 232, 305, 417, 92,
        95, 2, 64, 98, 6, 195,
        499, 48, 143, 16, 11, 111
    ],
    "Latitude": [
        10.7905, 25.7617, 19.0760, 40.4173, 44.2312, 13.0827, 16.5062, 53.4084,
        33.7490, 41.6085, 51.6019, 28.0345, 17.3850, 34.1706,
        50.9097, 14.6760, 38.8339, 52.0629, 54.5742,
        52.9225, 32.7767, 33.5207, 38.2527, 55.0068, 12.9716,
        39.7285, 32.7688, 54.5964, 42.3751, 10.3157, 28.4595,
        40.7608, 55.9533, 53.4808, 35.0456, 27.9506, 42.2711,
        19.4326, 11.9416, 37.8390, 39.9612, 38.5201, -37.8136
    ],
    "Longitude": [
        78.7047, -80.1918, 72.8777, -82.9071, -76.4859, 80.2707, 80.6480, -2.9916,
        -84.3880, -86.7253, -3.3425, -80.5887, 78.4867, -118.8376,
        -1.4043, 121.0437, -104.8214, -1.3409, -1.2350,
        -1.4750, -96.7969, -86.8025, -85.7585, -7.3163, 77.5946,
        -121.8363, -97.3095, -5.9301, -72.5199, 123.8854, 77.0266,
        -111.8910, -3.1883, -2.2426, -85.3097, -82.4572, -89.0937,
        -99.1332, 79.8083, -94.7050, -82.9988, -90.0473, 144.9631
    ]
})

# Create the geospatial map
fig = px.scatter_geo(
    location_data,
    lat="Latitude",
    lon="Longitude",
    size="Count",
    hover_name="Location",
    title="Geospatial Distribution of Employees",
    projection="natural earth"
)

# Display the map
st.plotly_chart(fig)
