#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import pickle


st.title('Flavor Recommendation')


df = pd.read_pickle("asset/cleaned_wines.pkl")

@st.cache
def recommend_flavor(flavor_matrix):
    # Find the wines with a similar cosine-sim value and order them from bigges number    
    distances = cdist(flavor_matrix.reshape(1, -1), df.iloc[:,10:], 'cosine')

    # Extract top 30 wine indexes with a similar cosine-sim value
    top30_indexes = list(np.argsort(distances)[:, :30][0])

    # Creating the new data set to show similar wines
    df_new = pd.DataFrame()
    for each in top30_indexes:
        df_new = df_new.append(pd.DataFrame(df[df.index == each]))

    # Sort only the top 10 by the highest rating
    df_new = df_new.sort_values(by='rating', ascending=False).head(10)
    # print('Top wines with similar reviews according to the user list: ')
    return df_new


st.header('Rank your flavor preference!')

flavor_d = {'black_fruit':0, 'citrus_fruit':0, 'dried_fruit':0, 'earth':0, 'floral':0,
           'microbio':0, 'non_oak':0, 'oak':0, 'red_fruit':0, 'spices':0, 'tree_fruit':0,'tropical_fruit':0, 'vegetal':0}
    
flavor_1 = st.selectbox('Select your 1st preference:',('black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral',
           'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit','tropical_fruit', 'vegetal'))
st.write('You top 1 flavor:', flavor_1)

flavor_2 = st.selectbox('Select your 2nd preference:',('black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral',
           'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit','tropical_fruit', 'vegetal'))
st.write('You top 2 flavor:', flavor_2)

flavor_3 = st.selectbox('Select your 3rd preference:',('black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral',
           'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit','tropical_fruit', 'vegetal'))
st.write('You top 3 flavor:', flavor_3)

flavor_4 = st.selectbox('Select your 4th preference:',('black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral',
           'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit','tropical_fruit', 'vegetal'))
st.write('You top 4 flavor:', flavor_4)

flavor_5 = st.selectbox('Select your 5th preference:',('black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral',
           'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit','tropical_fruit', 'vegetal'))
st.write('You top 5 flavor:', flavor_5)

flavor_d[flavor_1] = 10/25
flavor_d[flavor_2] = 6/25
flavor_d[flavor_3] = 4/25
flavor_d[flavor_4] = 3/25
flavor_d[flavor_5] = 2/25
flavor_matrix = np.array(list(flavor_d.values()))

gd2 = GridOptionsBuilder.from_dataframe(recommend_flavor(flavor_matrix))
gd2.configure_grid_options(rowHeight=60)
gd2.configure_column('index', hide=True)
gd2.configure_column(
    'image'
)
gd2.configure_column(
    'image',
    cellRenderer=JsCode('''
    function(params) {
        return '<a href="' + params.value + '" target="_blank">' + '<img src="' + params.value + '" width="60" >' + '</a>'
    };
    ''')
)

gridoptions2 = gd2.build()
ok = st.button("Make Recommendation")
if ok:
    recomendation_list = recommend_flavor(flavor_matrix) 
    AgGrid(recomendation_list, gridOptions = gridoptions2, columns_auto_size_mode='FIT_CONTENTS')
    st.success('Done!')
    st.session_state['recomend'] = recomendation_list

