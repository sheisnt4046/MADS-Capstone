import streamlit as st
import plotly

st.title('Visualization')

@st.cache
def read_chart(title):
    return plotly.io.read_json("plotly/%s.json" % title)

st.subheader("Visualization of the K-means clusters (k=32) by t-SNE transformation")
st.caption('T-Distributed Stochastic Neighbor Embedding (t-SNE) well separates most clusters while losing some information about inter-cluster relationships.')
fig1 = read_chart("t-SNE")
st.plotly_chart(fig1)

st.subheader("Visualization of the K-means clusters (k=32) by MDS transformation")
st.caption('Multidimensional Scaling (MDS) visualizes the clusters with preserved intra-cluster distances and shows some equivocal instances around the cluster margins.')
fig2 = read_chart("MDS")
st.plotly_chart(fig2)

st.subheader("Visualization of the K-means clusters (k=32) by PCA transformation")
st.caption('Principal Components Analysis (PCA) demonstrates two major branches of the wines with a contact zone in which there are multiple indistinguishable clusters.')
fig3 = read_chart("PCA")
st.plotly_chart(fig3)