import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from nltk.corpus import stopwords
from wordcloud import WordCloud
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from time import sleep


st.title('Wordcloud')
chosen_list = st.radio(
    "Which list to generate Wordcloud",
    ('Favorite List', 'Recomenede List'))

if chosen_list == 'Favorite List':
    st.write('Select Favorite List:')
    df = st.session_state['favorite']
else:
    st.write("Select Recomenede List:")
    df = st.session_state['recomend']

gd2 = GridOptionsBuilder.from_dataframe(df)
gd2.configure_grid_options(rowHeight=60)
gd2.configure_column('index', hide=True)
gd2.configure_column(
    'image',
    cellRenderer=JsCode('''
    function(params) {
        return '<a href="' + params.value + '" target="_blank">' + '<img src="' + params.value + '" width="60" >' + '</a>'
    };
    ''')
)
gridoptions2 = gd2.build()
AgGrid(df, gridOptions = gridoptions2, allow_unsafe_jscode = True, columns_auto_size_mode='FIT_CONTENTS')


def get_wine_data(wine_id, year, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }
    api_url = "https://www.vivino.com/api/wines/{id}/reviews?per_page=50&year={year}&page={page}"
    data = requests.get(
        api_url.format(id=wine_id, year=year, page=page), headers=headers
    ).json()

    return data

def get_text(df=df):
    text = ''
    for _, row in df.iterrows():
        page = 1
        while True:
            d = get_wine_data(row["wine ID"], row["year"], page)
            try:
                for r in d["reviews"]:
                    if r["language"] != "en": # <-- get only english reviews
                        continue

                    text += r["note"]
                    text += ' '
            except:
                break
            if page == 2:
                break
            page += 1
    return text

add_stopwords = {'well', 'nice', 'good', 'excellent', 'better', 'big', 'great', 'well', 'really', 
                 'taste', 'note', 'notes', 'nose', 'palate', 'aroma', 'flavor', 'color', 'body',
                 'finish', 'year', 'drink', 'long', 'still', 'like', 'one', 'hint', 'hour', 'month', 'bit',
                 'wine', 'bottle'}
stopwords_list = list(set(stopwords.words('english')) | set(stopwords.words('french')) | set(stopwords.words('italian')) | set(stopwords.words('german')) | set(stopwords.words('portuguese')) | set(stopwords.words('spanish')) | add_stopwords)


def make_wordcloud(text, stop_words, mask):
    wine_mask = np.array(Image.open(mask))
    wordcloud = WordCloud(width = 1200, height = 1200, stopwords=stop_words, scale=10, 
                        colormap = 'YlOrRd', background_color ='black', mask=wine_mask, max_words=100).generate(text)
    fig, ax = plt.subplots(figsize = (10, 10))
    ax.imshow(wordcloud)
    ax.axis("off")
    plt.show()
    st.pyplot(fig)

ok = st.button("Make Wordcloud")
if ok:   
    with st.spinner('Getting reviews...'):
        text = get_text(df)
    with st.spinner('Making Wordcloud...'):
        make_wordcloud(text, stopwords_list, "picture/wine_image.jpg")
    st.success('Done!')
    