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

    # Replace NULL values with "Unknown"
    df.fillna("Unknown", inplace=True)

    # Sidebar Slicers
    st.sidebar.header("Filters")
    grade_slicer = st.sidebar.multiselect("Grade", options=df["Grade"].unique(), default=df["Grade"].unique())
    designation_slicer = st.sidebar.multiselect("Designation", options=df["Designation"].unique(), default=df["Designation"].unique())
    estate_slicer = st.sidebar.multiselect("Estate", options=df["Estate"].unique(), default=df["Estate"].unique())
    buclassification_slicer = st.sidebar.multiselect("BUClassification", options=df["BUClassification"].unique(), default=df["BUClassification"].unique())
    vertical_slicer = st.sidebar.multiselect("Vertical", options=df["Vertical"].unique(), default=df["Vertical"].unique())
    location_slicer = st.sidebar.multiselect("Location", options=df["Location"].unique(), default=df["Location"].unique())
    employee_group_slicer = st.sidebar.multiselect("Employee Group", options=df["EmployeeGroup"].unique(), default=df["EmployeeGroup"].unique())

    # Apply filters to the DataFrame
    filtered_df = df[
        (df["Grade"].isin(grade_slicer)) &
        (df["Designation"].isin(designation_slicer)) &
        (df["Estate"].isin(estate_slicer)) &
        (df["BUClassification"].isin(buclassification_slicer)) &
        (df["Vertical"].isin(vertical_slicer)) &
        (df["Location"].isin(location_slicer)) &
        (df["EmployeeGroup"].isin(employee_group_slicer))
    ]

    # Display the filtered DataFrame
    st.dataframe(filtered_df)

    # Close the connection
    conn.close()

except pymssql.DatabaseError as e:
    st.error(f"Database connection failed: {e}")
