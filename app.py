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

    # Sidebar Filters (Dropdowns with default "All" functionality)
    st.sidebar.header("Filters")

    grade_filter = st.sidebar.selectbox(
        "Grade", options=["All"] + list(df["Grade"].unique()), index=0
    )
    designation_filter = st.sidebar.selectbox(
        "Designation", options=["All"] + list(df["Designation"].unique()), index=0
    )
    estate_filter = st.sidebar.selectbox(
        "Estate", options=["All"] + list(df["Estate"].unique()), index=0
    )
    buclassification_filter = st.sidebar.selectbox(
        "BUClassification", options=["All"] + list(df["BUClassification"].unique()), index=0
    )
    vertical_filter = st.sidebar.selectbox(
        "Vertical", options=["All"] + list(df["Vertical"].unique()), index=0
    )
    location_filter = st.sidebar.selectbox(
        "Location", options=["All"] + list(df["Location"].unique()), index=0
    )
    employee_group_filter = st.sidebar.selectbox(
        "Employee Group", options=["All"] + list(df["EmployeeGroup"].unique()), index=0
    )

    # Apply filters to the DataFrame
    filtered_df = df.copy()

    if grade_filter != "All":
        filtered_df = filtered_df[filtered_df["Grade"] == grade_filter]
    if designation_filter != "All":
        filtered_df = filtered_df[filtered_df["Designation"] == designation_filter]
    if estate_filter != "All":
        filtered_df = filtered_df[filtered_df["Estate"] == estate_filter]
    if buclassification_filter != "All":
        filtered_df = filtered_df[filtered_df["BUClassification"] == buclassification_filter]
    if vertical_filter != "All":
        filtered_df = filtered_df[filtered_df["Vertical"] == vertical_filter]
    if location_filter != "All":
        filtered_df = filtered_df[filtered_df["Location"] == location_filter]
    if employee_group_filter != "All":
        filtered_df = filtered_df[filtered_df["EmployeeGroup"] == employee_group_filter]

    # Display the filtered DataFrame
    st.dataframe(filtered_df)

    # Close the connection
    conn.close()

except pymssql.DatabaseError as e:
    st.error(f"Database connection failed: {e}")
