import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import pickle


st.title('Recommendation')


df = pd.read_pickle("asset/cleaned_noreviews.pkl")
df = df.reset_index(level=0)
with open('model/vectorizer.pkl', 'rb') as vectorizerfile:
    vectorizer = pickle.load(vectorizerfile)
with open('model/km.pkl', 'rb') as kmfile:
    km = pickle.load(kmfile)
X_ar = np.load('model/X_ar.npy')


@st.cache
def get_mean_vector(idx_list, km = km, X_ar = X_ar): 
    indices = pd.Series(df.index)
    vectors = []
    
    for wine in idx_list:
        idx = indices[indices == wine].index[0]
        vector = km.transform(X_ar[idx].reshape(1, -1))
        vectors.append(vector)  
    
    song_matrix = np.array(list(vectors))
    return np.mean(song_matrix, axis=0)


@st.cache
def recommend_knn(wine_list, km = km, X_ar = X_ar):
    # Find the wines with a similar cosine-sim value and order them from bigges number
    wine_data = km.transform(X_ar)
    wine_center = get_mean_vector(wine_list).reshape(1, -1)
    distances = cdist(wine_center, wine_data, 'cosine')

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


st.header('Select wines from the database!')
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(paginationAutoPageSize=True)
gd.configure_default_column(editable=True, groupable=True)
gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gd.configure_grid_options(rowHeight=60)
gd.configure_column(
    'image',
    cellRenderer=JsCode('''
    function(params) {
        return '<a href="' + params.value + '" target="_blank">' + '<img src="' + params.value + '" width="60" >' + '</a>'
    };
    ''')
)
gridoptions = gd.build()
grid_table = AgGrid(df, gridOptions = gridoptions,
                    update_mode ='SELECTION_CHANGED',
                    height = 800, 
                    allow_unsafe_jscode = True, 
                    columns_auto_size_mode='FIT_CONTENTS')


st.header('Your Wine List')
sel_row = grid_table['selected_rows']
sel_data = pd.DataFrame(sel_row).iloc[:,1:]
if len(sel_data)> 0 :
    sel_idx = sel_data['index'].to_list()

gd2 = GridOptionsBuilder.from_dataframe(sel_data)
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
AgGrid(sel_data, gridOptions = gridoptions2, allow_unsafe_jscode = True, columns_auto_size_mode='FIT_CONTENTS')
st.session_state['favorite'] = sel_data

ok = st.button("Make Recommendation")
if ok:
    recomendation_list = recommend_knn(sel_idx) 
    st.header('Your Recommend List')
    AgGrid(recomendation_list, gridOptions = gridoptions2, allow_unsafe_jscode = True, columns_auto_size_mode='FIT_CONTENTS')
    st.success('Done!')
    st.session_state['recomend'] = recomendation_list