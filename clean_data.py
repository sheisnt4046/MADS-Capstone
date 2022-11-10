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

    return cleaned_wine
    

def clean_reviews(df):
    df = df.groupby(['wine ID', 'year']).agg({
        'Review': lambda x : ' '.join(x),
        'country':'unique', 
        })
    df.reset_index(inplace=True)
    df['country'] = df['country'].apply(lambda x: x[0])
    wine_data = wines[['name', 'year', 'wine ID', 'rating', 'price', 'winery', 'image']]
    df = pd.merge(wine_data, df, on = ['wine ID', 'year'])
    return df


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('wine_data', help='wine data file (pkl)', type=str, default='asset/wines.pkl')
    parser.add_argument('review_data', help='review data file (pkl)', type=str, default='asset/reviews.pkl')
    parser.add_argument('cleaned_wine', help='output of cleaned wine data file (pkl)', type=str, default='asset/cleaned_wines.pkl')
    parser.add_argument('cleaned_review', help='output of cleaned review data file (pkl)', type=str, default='asset/cleaned_reviews.pkl')
    args = parser.parse_args()

    wines =  pd.read_pickle(args.wine_data)
    cleaned_wines = clean_wines(wines)
    cleaned_wines.to_pickle(args.cleaned_wine)
    reviews = pd.read_pickle(args.review_data)
    cleaned_reviews = clean_reviews(reviews)
    cleaned_reviews.to_pickle(args.cleaned_review)
