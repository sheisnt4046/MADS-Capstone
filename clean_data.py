import pandas as pd
import re
from sklearn.feature_extraction import DictVectorizer


flavors = ['black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral',
           'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit',
           'tropical_fruit', 'vegetal']

def clean_wines(df):
    df['flavors_in_wine'] = df['flavors_in_wine'].astype('string').apply(lambda x: dict(zip(re.findall('\'group\W*(.*?)\W', x), re.findall('stats\W*\'count\W*(.*?)\W', x))))
    data_dict = df['flavors_in_wine'].to_list()
    data_dict = [dict([a, int(x)] for a, x in b.items()) for b in data_dict]
    dictvectorizer = DictVectorizer(sparse=False)
    features = dictvectorizer.fit_transform(data_dict)
    feature_name =dictvectorizer.get_feature_names()
    df_flavor = pd.DataFrame(features, columns=feature_name)
    cleaned_wine = pd.merge(df, df_flavor, left_index=True, right_index=True)
    cleaned_wine = cleaned_wine.drop(columns=['flavors_in_wine'])
    #normalize the value of flavors by dividing ratings_count
    for flavor in flavors:
        cleaned_wine[flavor] = cleaned_wine[flavor]/cleaned_wine['ratings_count']
    cleaned_wine = cleaned_wine.astype({'name': 'string', 'year': 'category', 'country': 'category', 'image': 'string'})
    for col in cleaned_wine.select_dtypes('number'):
        cleaned_wine[col] = pd.to_numeric(cleaned_wine[col], downcast='integer')
        if cleaned_wine[col].dtype == 'float':
            cleaned_wine[col] = pd.to_numeric(cleaned_wine[col], downcast='float')
    cleaned_wine = cleaned_wine.replace(['None_Supplied'], 'https://www.freeiconspng.com/uploads/no-image-icon-21.png')
    return cleaned_wine
    

def clean_reviews(df):
    df = df.groupby(['wine ID', 'year']).agg({
        'Review': lambda x : ' '.join(x),
        'country':'unique', 
        })
    df.reset_index(inplace=True)
    df['country'] = df['country'].apply(lambda x: x[0])
    wine_data = wines[['name', 'year', 'wine ID', 'rating', 'price', 'winery', 'image']]
    for col in wine_data.select_dtypes('number'):
        wine_data[col] = pd.to_numeric(wine_data[col], downcast='integer')
        if wine_data[col].dtype == 'float':
            wine_data[col] = pd.to_numeric(wine_data[col], downcast='float')
    df = pd.merge(wine_data, df, on = ['wine ID', 'year'])
    df = df.astype({'name': 'string', 'year': 'category', 'winery': 'string', 'image': 'string', 'Review': 'string', 'country': 'category'})
    df = df.replace(['None_Supplied'], 'https://www.freeiconspng.com/uploads/no-image-icon-21.png')
    return df


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('wine_data', help='wine data file (pkl)', type=str, default='asset/wines.pkl')
    parser.add_argument('review_data', help='review data file (pkl)', type=str, default='asset/reviews.pkl')
    parser.add_argument('cleaned_wine', help='output of cleaned wine data file (pkl)', type=str, default='asset/cleaned_wines.pkl')
    parser.add_argument('cleaned_review', help='output of cleaned review data file (pkl)', type=str, default='asset/cleaned_reviews.pkl')
    parser.add_argument('cleaned_noreview', help='output of cleaned review data (without Review column) file (pkl)', type=str, default='asset/cleaned_noreviews.pkl')
    args = parser.parse_args()

    wines =  pd.read_pickle(args.wine_data)
    cleaned_wines = clean_wines(wines)
    cleaned_wines.to_pickle(args.cleaned_wine)
    reviews = pd.read_pickle(args.review_data)
    cleaned_reviews = clean_reviews(reviews)
    cleaned_reviews.to_pickle(args.cleaned_review)
    cleaned_noreviews = cleaned_reviews.drop('Review', axis = 1)
    cleaned_noreviews.to_pickle(args.cleaned_noreview)
