import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import pickle


st.title('Flavor Recommendation')

option = st.selectbox(
        "Which flavor would you like to know more about?",
        ('Black Fruit', 'Citrus Fruit', 'Dried Fruit', 'Earth', 'Floral',
        'Microbio', 'Non-oak', 'Oak', 'Red Fruit', 'Spicy', 'Tree Fruit','Tropical Fruit', 'Vegetal'),
        label_visibility="visible",
        disabled=False,
    )

if option == 'Black Fruit':
    display_text = "Simply enough, most black fruit actually has the word “black” in the name—blackberry, \
                    black cherry, and blackcurrant."
if option == 'Citrus Fruit':
    display_text = "Lemons, limes, grapefruits, and oranges, mostly. It’s often an indicator that the wine is from a cooler-climate. \
                    Grapes there don’t ripen as fully as in warmer climates, and therefore they tend to show these cleaner, leaner, \
                    dare we say refreshing citrus notes."
if option == 'Dried Fruit':
    display_text = "Imagine the delight of the earliest senses at the chewy sweet rush of flavor delivered by a date, \
                    a prune, or a fig, its essence concentrated by sunlight."
if option == 'Earth':
    display_text = "There’s no dirt in your wine, we promise. But these secondary aromas can exist alongside other notes. \
                    They can result from the winemaking process or because of the wine’s terroir, \
                    and they can be an indicator of age. These might be aromas of dirt or the forest floor."
if option == 'Floral':
    display_text = "Floral is found in both red and white wines, and it is just what it sounds like. \
                    Viognier is a classic example of a wine with white floral aromas—typically honeysuckle. \
                    Pinot Noir and well-crafted Bordeaux blends often have perfumes hinting at dried flowers, like roses and violets. Sniff on!"
if option == 'Microbio':
    display_text = "There’s no mushrooms in your wine, we promise. But these secondary aromas can exist alongside other notes. \
                    They can result from the winemaking process or because of the wine’s terroir, and they can be an indicator of age. \
                    These might be aromas of  various mushrooms or truffles."
if option == 'Non-oak':
    display_text = "Picture that you have a filet of nice white fish. You can have it raw (the equivalent of the grape itself) or \
                    you can bake it in the oven with a bit of lemon and salt, en papillotte (unoaked simple and fruity wine). \
                    It will taste nice, because the fish is good quality and fresh. And this can be the perfect choice sometimes."
if option == 'Oak':
    display_text = "Wines that are aged in oak barrels will most assuredly smell and taste like that oak, especially if it was a brand new barrel. \
                    Plus, wine barrels are often toasted (yes, with fire) on in the inside, so along with oak, \
                    you might experience secondary flavors like graham cracker crust, pie crust, tobacco, smoke, or vanilla."
if option == 'Red Fruit':
    display_text = "If a wine is described as having a red fruit flavors and aromas that means, \
                    apart from the grapes, there is a strong sense of red berry flavors, most often strawberries, cherries, raspberries and pomegranate."
if option == 'Spicy':
    display_text = "When a chef wants spice in a dish, they go to their spice rack. When a winemaker wants spice, they turn to oak barrels. \
                    These spice notes can be savory like black pepper or sweet, like the cinnamon/clove/nutmeg-esque baking spice aromas."
if option == 'Tree Fruit':
    display_text = "Think apricots, peaches, apples, pears, and plums. Even if you can’t pinpoint the exact variety you’re tasting, \
                    you’ll likely notice this juicy note in richer whites and rosé wines."
if option == 'Tropical Fruit':
    display_text = "You know these from your vacations on the Big Island or the Bahamas. White grapes grown in hotter limates \
                   (regions like the warmest areas of California, Chile, Argentina, Italy, and Australia), \
                    tend to produce tropical fruit notes like pineapple, papaya, and passion fruit."
if option == 'Vegetal':
    display_text = "Green notes like bell peppers, asparagus, freshly cut grass, or herbs like rosemary, sage and thyme. \
                    Two classic examples are Loire Valley Cabernet Franc, which has aromas of green pepper, \
                    and New Zealand Sauvignon Blanc, with its aromatic jalapeño and grassy character."

st.write(display_text)

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
    return df_new[['name', 'year', 'wine ID', 'rating', 'price', 'winery', 'ratings_count', 'country', 'image']]


st.header('Rank your flavor preference!')

flavor_d = {'Black Fruit':0, 'Citrus Fruit':0, 'Dried Fruit':0, 'Earth':0, 'Floral':0,
           'Microbio':0, 'Non-oak':0, 'Oak':0, 'Red Fruit':0, 'Spicy':0, 'Tree Fruit':0,'Tropical Fruit':0, 'Vegetal':0}
flavor_t = ('Black Fruit', 'Citrus Fruit', 'Dried Fruit', 'Earth', 'Floral',
        'Microbio', 'Non-oak', 'Oak', 'Red Fruit', 'Spicy', 'Tree Fruit','Tropical Fruit', 'Vegetal')

flavor_1 = st.selectbox('Select your 1st preference:', flavor_t)
st.caption('Your 1st pick:' + flavor_1)
flavor_2 = st.selectbox('Select your 2nd preference:', tuple(flavor for flavor in flavor_t if flavor != flavor_1))
st.caption('Your 2nd pick:' + flavor_2)
flavor_3 = st.selectbox('Select your 3rd preference:', tuple(flavor for flavor in flavor_t if flavor not in [flavor_1, flavor_2]))
st.caption('Your 3rd pick:' + flavor_3)
flavor_4 = st.selectbox('Select your 4th preference:', tuple(flavor for flavor in flavor_t if flavor not in [flavor_1, flavor_2, flavor_3]))
st.caption('Your 4th pick:' + flavor_4)
flavor_5 = st.selectbox('Select your 5th preference:',tuple(flavor for flavor in flavor_t if flavor not in [flavor_1, flavor_2, flavor_3, flavor_4]))
st.caption('Your 5th pick:' + flavor_5)

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
    AgGrid(recomendation_list, gridOptions = gridoptions2, allow_unsafe_jscode = True, columns_auto_size_mode='FIT_CONTENTS')
    st.success('Done!')
    st.session_state['flavor'] = recomendation_list