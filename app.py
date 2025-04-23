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

    # Display the DataFrame
    st.dataframe(df)

    # Function to generate and display a bar chart for a given column
    def generate_bar_chart(column_name):
        grouped_data = df[column_name].value_counts().reset_index()  # Group by column and count
        grouped_data.columns = [column_name, 'Count']  # Rename columns for clarity
        fig = px.bar(grouped_data, x=column_name, y='Count', title=f"{column_name} vs Count")
        st.plotly_chart(fig)

    # Generate and display graphs for each parameter (excluding Gender)
    st.header("Graphs for Each Parameter vs Count")
    generate_bar_chart("Grade")
    generate_bar_chart("Designation")
    generate_bar_chart("Estate")
    generate_bar_chart("BUClassification")
    generate_bar_chart("Vertical")
    generate_bar_chart("Location")
    generate_bar_chart("EmployeeGroup")

    # Close the connection
    conn.close()

except pymssql.DatabaseError as e:
    st.error(f"Database connection failed: {e}")
