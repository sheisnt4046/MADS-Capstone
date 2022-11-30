import streamlit as st


st.set_page_config(
    page_title = 'Wine Roadmap',
    page_icon = '🍷'
)


st.sidebar.success('Select a page.')

st.title('Wine Roadmap')
st.header(“Life is struggle, you deserve a wine”)

st.markdown("""
This website is designed for both **wine beginners** and **wine lovers**.

If you are a person who has no idea which wine to be your first choice, go to 🍇_Flavor page.

If you are a person who has already had your own wine testing preference list, go to 👍_Recommendation page.

After you click **make recommendation**. You can go to 💭_Wordcloud page to take a look at your result.

Also, we provide 🗺️_Visualization page to visualize PCA, t-SNE, and MDS.

""")
