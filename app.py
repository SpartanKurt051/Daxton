import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns

# MSSQL Database Connection
def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=your_server;'
        'DATABASE=your_database;'
        'UID=your_username;'
        'PWD=your_password;'
    )
    return conn

# Load Data from MSSQL
@st.cache
def load_data():
    conn = get_connection()
    query = "SELECT Grade, Designation, Gender, [Estate (Cluster)], BUClassification, Vertical, Location, EmployeeGroup FROM employees"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load Data
df = load_data()

# Streamlit App
st.title("Employee Data Visualization")

# Graphs for Each Column
columns = ['Grade', 'Designation', 'Gender', 'Estate (Cluster)', 'BUClassification', 'Vertical', 'Location', 'EmployeeGroup']

for col in columns:
    st.subheader(f"Graph for {col}")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x=col, order=df[col].value_counts().index, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
