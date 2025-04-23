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

    # Function to generate and display pie charts with percentages inside
    def generate_side_by_side_pie_charts(column_names):
        col1, col2 = st.columns(2)  # Divide the page into two columns

        # Iterate through the columns and generate graphs
        for i, column_name in enumerate(column_names):
            grouped_data = df[column_name].value_counts().reset_index()  # Group by column and count
            grouped_data.columns = [column_name, 'Count']  # Rename columns for clarity
            fig = px.pie(grouped_data, names=column_name, values='Count', title=f"{column_name} Distribution")

            # Display percentages and labels inside the pie chart
            fig.update_traces(textinfo='percent+label', textposition='inside')  # Percentages inside the chart

            # Alternate between columns
            if i % 2 == 0:  # If index is even, use col1
                with col1:
                    st.plotly_chart(fig)
            else:  # If index is odd, use col2
                with col2:
                    st.plotly_chart(fig)

    # Geospatial graph for Location with preprocessing
    def generate_geospatial_location_map():
        # Preprocess the Location column to ensure valid geographic names
        location_data = df['Location'].value_counts().reset_index()
        location_data.columns = ['Location', 'Count']

        # Check for invalid or unrecognized locations and map them to valid names if needed
        # Example: Custom mapping for specific abbreviations or invalid entries
        location_mapping = {
            "MX": "Mexico",
            "US": "United States",
            # Add more mappings here if necessary
        }
        location_data['Location'] = location_data['Location'].replace(location_mapping)

        # Create the geospatial map
        fig = px.scatter_geo(location_data, locations="Location", locationmode="country names",
                             size="Count", title="Geospatial Distribution of Employees")
        st.plotly_chart(fig)

    # Generate and display pie charts for each parameter except Location
    st.header("Pie Charts for Each Parameter")
    columns_to_plot = ["Grade", "Designation", "Estate", "BUClassification", "Vertical", "EmployeeGroup"]
    generate_side_by_side_pie_charts(columns_to_plot)

    # Generate and display geospatial graph for Location
    st.header("Geospatial Graph for Location")
    generate_geospatial_location_map()

    # Close the connection
    conn.close()

except pymssql.DatabaseError as e:
    st.error(f"Database connection failed: {e}")
