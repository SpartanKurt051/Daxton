import pymssql
import pandas as pd
import streamlit as st

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

    # Display the DataFrame in Streamlit
    st.dataframe(df)

    # Create slicers in the sidebar for the 7 parameters (excluding Gender)
    st.sidebar.header("Filters")
    grade_slicer = st.sidebar.multiselect("Grade", options=df["Grade"].unique())
    designation_slicer = st.sidebar.multiselect("Designation", options=df["Designation"].unique())
    estate_slicer = st.sidebar.multiselect("Estate", options=df["Estate"].unique())
    buclassification_slicer = st.sidebar.multiselect("BUClassification", options=df["BUClassification"].unique())
    vertical_slicer = st.sidebar.multiselect("Vertical", options=df["Vertical"].unique())
    location_slicer = st.sidebar.multiselect("Location", options=df["Location"].unique())
    employee_group_slicer = st.sidebar.multiselect("Employee Group", options=df["EmployeeGroup"].unique())

    # Currently, slicers have no functionality applied to the DataFrame.

    # Close the connection
    conn.close()

except pymssql.DatabaseError as e:
    st.error(f"Database connection failed: {e}")
