import plotly.graph_objects as go
import streamlit as st

fig = go.Figure(data=[go.Pie(
    labels=['A', 'B', 'C'],
    values=[30, 50, 20],
    hole=0.3,  # donut effect
    marker=dict(
        colors=['#FF007F', '#00FFFF', '#8A2BE2'],
        line=dict(color='#000000', width=2)
    )
)])
fig.update_layout(
    title="Synthwave Style Pie",
    paper_bgcolor="#000000",
    font=dict(color='white')
)

st.plotly_chart(fig)
