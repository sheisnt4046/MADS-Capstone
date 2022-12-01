import streamlit as st


st.set_page_config(
    page_title = 'Wine Roadmap',
    page_icon = '🍷'
)


st.sidebar.success('Select a page.')

st.title('Wine Roadmap')

st.markdown("""
## This website is designed for both **wine beginners** and **wine lovers**.

### If you are a person who has no idea which wine to be your first choice
### --> click 🍇_Flavor page

In the 🍇_Flavor page, you can find 13 different wine flavors. Try to rank your flavor preference. We will recommend suitable wine based on your choice.

Once you click **make recommendation** and get the wine list, you can go to 💭_Wordcloud page. In the 💭_Wordcloud page, choose **Flavor Formula**, and click **Make Wordcloud**. Then, we will generate word cloud for you based on your preference.

Tips: you can either 
1.	follow the recommendation list we provided for you OR
2.	search words from the word cloud as the keyword on the Internet OR
3.	click 🗺️_Visualization page and find the cluster, which keywords also show on your word cloud. Also, you can refer the closer cluster as well since the flavor might be similar and perhaps could be one of your choices.

### If you are a person who has already had your own wine testing preference list
### --> click 👍_Recommendation page

In the 👍_Recommendation page, there is a dataframe which contains all wines on the Vivino website. You can search and find your favorite wine. If you check a wine, you will find the wine you pick will show on the **Your Wine List**.

Once you click **make recommendation** and get the wine list, you can go to 💭_Wordcloud page. In the 💭_Wordcloud page, you can choose either **Favorite List** or **Recommend List**. 
If you choose **Favorite List** and click **Make Wordcloud**. Then, we will generate word cloud for you based on wines on your favorite list, which is **Your Wine List** on the 👍_Recommendation page.
If you choose **Recommend List** and click **Make Wordcloud**. Then, we will generate word cloud for you based on wines we recommend for you, which is ** Your Recommend List** on the 👍_Recommendation page.


Tips: you can
1.	Save wordcloud images of both Favorite List and Recommend List. Compare two wordcloud to see the similarity and difference. OR
2.	click 🗺️_Visualization page and find the cluster, which keywords also show on your word cloud. Also, you can refer the closer cluster as well since the flavor might be similar and perhaps could be one of your choices.

### Hope you enjoy this website. Life is struggle, you deserve a wine
""")

