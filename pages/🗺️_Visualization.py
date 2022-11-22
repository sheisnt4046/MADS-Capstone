import streamlit as st
import plotly

st.title('Visualization')

@st.cache
def read_chart(title="t-SNE"):
    return plotly.io.read_json("plotly/%s.json" % title)

fig = read_chart("t-SNE")
st.plotly_chart(fig)

fig = read_chart("MDS")
st.plotly_chart(fig)

fig = read_chart("PCA")
st.plotly_chart(fig)

