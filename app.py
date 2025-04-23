import pymssql
import pandas as pd
import streamlit as st

# MSSQL Connection Details
server = '103.171.180.23'
user = 'mpdx_user'
password = '9xpeiFpg5M5vaf9#L'
database = 'ManPlanDx'

# Streamlit App Title
st.title("Employee Details from ManPlanDx Database")

try:
    # Connect to the MSSQL Database
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()

    # Query to fetch data from Employees table
    query = """
    SELECT Grade, Designation, Gender, [Estate (Cluster)], BUClassification, Vertical, Location, EmployeeGroup
    FROM Employees
    """
    # Execute the query
    cursor.execute(query)

    # Fetch all rows and load into a pandas DataFrame
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # Get column names
    df = pd.DataFrame(data, columns=columns)

    # Close the database connection
    conn.close()

    # Slicers
    st.sidebar.header("Filters")  # Add a header for the slicers in the sidebar

    # Create slicers for each column
    grade_filter = st.sidebar.multiselect("Select Grade", options=df["Grade"].unique(), default=df["Grade"].unique())
    designation_filter = st.sidebar.multiselect("Select Designation", options=df["Designation"].unique(), default=df["Designation"].unique())
    gender_filter = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
    estate_filter = st.sidebar.multiselect("Select Estate (Cluster)", options=df["Estate (Cluster)"].unique(), default=df["Estate (Cluster)"].unique())
    buclassification_filter = st.sidebar.multiselect("Select BUClassification", options=df["BUClassification"].unique(), default=df["BUClassification"].unique())
    vertical_filter = st.sidebar.multiselect("Select Vertical", options=df["Vertical"].unique(), default=df["Vertical"].unique())
    location_filter = st.sidebar.multiselect("Select Location", options=df["Location"].unique(), default=df["Location"].unique())
    employee_group_filter = st.sidebar.multiselect("Select Employee Group", options=df["EmployeeGroup"].unique(), default=df["EmployeeGroup"].unique())

    # Apply filters to the DataFrame
    filtered_df = df[
        (df["Grade"].isin(grade_filter)) &
        (df["Designation"].isin(designation_filter)) &
        (df["Gender"].isin(gender_filter)) &
        (df["Estate (Cluster)"].isin(estate_filter)) &
        (df["BUClassification"].isin(buclassification_filter)) &
        (df["Vertical"].isin(vertical_filter)) &
        (df["Location"].isin(location_filter)) &
        (df["EmployeeGroup"].isin(employee_group_filter))
    ]

    # Display the filtered DataFrame
    st.dataframe(filtered_df)

except pymssql.DatabaseError as e:
    st.error(f"Database connection failed: {e}")
