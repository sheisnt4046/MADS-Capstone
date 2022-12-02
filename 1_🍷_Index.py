import streamlit as st


st.set_page_config(
    page_title = 'Wine Roadmap',
    page_icon = '🍷'
)


st.sidebar.success('Select a page.')

st.title('Wine Roadmap')

st.markdown("""
### This application is designed for both **wine beginners** and **wine lovers**.

#### If you have no idea which wine to be your first choice --> click 🍇Flavor page

On the 🍇Flavor page, you can find 13 different wine flavors. Try to rank your flavor preference. We will recommend suitable wine based on your choice.

Once you click `make recommendation` and get the wine list, you can go to 💭Wordcloud page. In the 💭Wordcloud page, choose `Flavor Formula`, and click `Make Wordcloud`. Then, we will generate Wordcloud for you based on your preference.

Tips: you can either 
1.	Follow the recommendation list we provided for you *OR*
2.	Search words from the word cloud as the keyword on the Internet *OR*
3.	Click 🗺️Visualization page and find the cluster, which keywords also show on your word cloud. Also, you can refer to the closest cluster since the flavor might be similar and perhaps could be one of your choices.

#### If you already have your own wine testing preference list --> click 👍Recommendation page

On the 👍Recommendation page, there is a dataframe which contains all wines on the Vivino website. You can search and find your favorite wine. If you check a wine, you will find the wine you pick will show on the `Your Wine List`.

Once you click `make recommendation` and get the wine list, you can go to 💭Wordcloud page. On the 💭Wordcloud page, you can choose either `Favorite List` or `Recommend List`. 

Suppose you choose `Favorite List` and click `Make Wordcloud`. Then, we will generate Wordcloud for you based on wines on your favorite list, which is `Your Wine List` on the 👍Recommendation page.

Suppose you choose `Recommend List` and click `Make Wordcloud`. Then, we will generate Wordcloud for you based on wines we recommend for you, which is `Your Recommend List` on the 👍Recommendation page.


Tips: you can either
1.	Save Wordcloud images of both Favorite List and Recommend List. Compare two Wordcloud to see the similarity and differences. *OR*
2.	Click 🗺️Visualization page and find the cluster, which keywords also show on your word cloud. Also, you can refer to the closest cluster since the flavor might be similar and perhaps could be one of your choices.

#### Hope you enjoy this website. Life is a struggle, you deserve wine!
""")

