import streamlit as st
import pymssql
import pandas as pd
import plotly.express as px

# Set Streamlit page layout to wide
st.set_page_config(layout="wide")

# MSSQL Connection Details
server = '103.171.180.23'
user = 'mpdx_user'
password = '9xpeiFpg5M5vaf9#L'
database = 'ManPlanDx'

# Function to generate pie charts
def generate_pie_chart(column_name, df):
    grouped_data = df[column_name].value_counts().reset_index()
    grouped_data.columns = [column_name, 'Count']
    fig = px.pie(grouped_data, names=column_name, values='Count')
    fig.update_traces(textinfo='percent+label', textposition='inside')  # Percentages inside the chart
    return fig

# Geospatial graph for Location
def generate_geospatial_location_map():
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

    fig = px.scatter_geo(
        location_data,
        lat="Latitude",
        lon="Longitude",
        size="Count",
        hover_name="Location",
        hover_data={"Count": True, "Latitude": False, "Longitude": False},
        projection="natural earth"
    )
    fig.update_layout(
        geo=dict(
            bgcolor='black',
                showcoastlines=True,
                coastlinecolor="green",
                showland=True,
                landcolor="black",
                showlakes=True,
                lakecolor="black",
                showocean=True,
                oceancolor="black",
                projection_type="natural earth",
                lonaxis=dict(gridcolor="goldenrod"),
                lataxis=dict(gridcolor="goldenrod")
        ),
        paper_bgcolor="black",
        plot_bgcolor="black",
        width=2500,
        height=700,
        font=dict(color="goldenrod")
    )
    fig.update_traces(marker=dict(color="#00FF00"))
    return fig

# Parse URL parameters
params = st.experimental_get_query_params()  # Fetch query parameters
graph = params.get('graph', [''])[0]  # Get the 'graph' parameter from the URL

# Connect to the MSSQL Database
try:
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()

    # Query to fetch data from Employees table
    query = """
    SELECT Grade, Designation, Gender, Estate, BUClassification, Vertical, Location, EmployeeGroup
    FROM Employees
    """
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    df.fillna("Unknown", inplace=True)

    # Conditional rendering based on the 'graph' query parameter
    if graph == 'grade_distribution':
        st.title("Grade Distribution")
        fig = generate_pie_chart("Grade", df)
        st.plotly_chart(fig)

    elif graph == 'designation_distribution':
        st.title("Designation Distribution")
        fig = generate_pie_chart("Designation", df)
        st.plotly_chart(fig)

    elif graph == 'estate_distribution':
        st.title("Estate Distribution")
        fig = generate_pie_chart("Estate", df)
        st.plotly_chart(fig)

    elif graph == 'bu_classification_distribution':
        st.title("BU Classification Distribution")
        fig = generate_pie_chart("BUClassification", df)
        st.plotly_chart(fig)

    elif graph == 'vertical_distribution':
        st.title("Vertical Distribution")
        fig = generate_pie_chart("Vertical", df)
        st.plotly_chart(fig)

    elif graph == 'employee_group_distribution':
        st.title("Employee Group Distribution")
        fig = generate_pie_chart("EmployeeGroup", df)
        st.plotly_chart(fig)

    elif graph == 'geospatial_location_map':
        st.title("Geospatial Graph for Location")
        fig = generate_geospatial_location_map()
        st.plotly_chart(fig)

    else:
        st.write("Please specify a valid graph using the 'graph' query parameter.")

except pymssql.Error as e:
    st.error(f"Database connection failed: {e}")

finally:
    if 'conn' in locals() and conn:
        conn.close()
