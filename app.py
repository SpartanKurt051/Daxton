import pymssql
import pandas as pd
import streamlit as st
import plotly.express as px

# MSSQL Connection Details
server = '103.171.180.23'
user = 'mpdx_user'
password = '9xpeiFpg5M5vaf9#L'
database = 'ManPlanDx'

# Streamlit App
st.title("Employee Details from ManPlanDx Database")

# Connect to the MSSQL Database
try:
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()

    # Query to fetch data from Employees table
    query = """
    SELECT Grade, Designation, Gender, Estate, BUClassification, Vertical, Location, EmployeeGroup
    FROM Employees
    """
    # Execute the query
    cursor.execute(query)

    # Fetch all rows and load into a pandas DataFrame
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # Get column names
    df = pd.DataFrame(data, columns=columns)

    # Replace NULL values with "Unknown"
    df.fillna("Unknown", inplace=True)

    # Function to preprocess and map locations
    def preprocess_locations(location_data):
        # Print unique locations for debugging
        st.write("Unique Locations Before Mapping:", location_data['Location'].unique())

        # Mapping custom or invalid location names to valid geographic names
        location_mapping = {
            "MX": "Mexico",
            "US": "United States",
            "NY": "New York",
            # Add more mappings here as needed
        }
        location_data['Location'] = location_data['Location'].replace(location_mapping)

        # Print unique locations after mapping
        st.write("Unique Locations After Mapping:", location_data['Location'].unique())

        return location_data

    # Geospatial graph for Location
    def generate_geospatial_location_map():
        # Preprocess the Location column to ensure valid geographic names
        location_data = df['Location'].value_counts().reset_index()
        location_data.columns = ['Location', 'Count']
        location_data = preprocess_locations(location_data)

        # Create the geospatial map
        fig = px.scatter_geo(location_data, locations="Location", locationmode="country names",
                             size="Count", title="Geospatial Distribution of Employees")
        st.plotly_chart(fig)

    # Generate and display geospatial graph for Location
    st.header("Geospatial Graph for Location")
    generate_geospatial_location_map()

    # Close the connection
    conn.close()

except pymssql.DatabaseError as e:
    st.error(f"Database connection failed: {e}")
