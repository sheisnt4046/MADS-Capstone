import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pickle


nltk.download('stopwords')
add_stopwords = {'well', 'nice', 'good', 'excellent', 'better', 'big', 'great', 'well', 'really', 
                 'taste', 'note', 'notes', 'nose', 'palate', 'aroma', 'flavor', 'color', 'body',
                 'finish', 'year', 'drink', 'long', 'still', 'like', 'one', 'hint', 'hour', 'month', 'bit',
                 'wine', 'bottle'}
stopwords_list = list(set(stopwords.words('english')) | set(stopwords.words('french')) | set(stopwords.words('italian')) | set(stopwords.words('german')) | set(stopwords.words('portuguese')) | set(stopwords.words('spanish')) | add_stopwords)


def get_reviews_vectorized(df, top_n=-1, ngram_range=(1, 1), max_features=1000):
    review_instances = df.Review.replace('\d+'," ", regex=True)
    review_instances = review_instances.replace(r'\n',' ', regex=True)

    vectorizer = TfidfVectorizer(
        max_df=0.5,
        max_features=max_features,
        min_df=15,
        stop_words=stopwords_list,
        ngram_range=ngram_range,
        use_idf=True,
    )
    if top_n >= 0:
        review_instances = review_instances.values[0:top_n]
        df = df[0:top_n]
    else:
        review_instances = review_instances.values

    X = vectorizer.fit_transform(review_instances)

    return (X, vectorizer)

def kmeans(X_ar, k_val = 32, random_state=42):
    km = KMeans(n_clusters=k_val, init='k-means++', max_iter=100, n_init=1, random_state=random_state).fit(X_ar)  
    return km


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('cleaned_review', help='cleaned review data file (pkl)', type=str, default='asset/cleaned_reviews.pkl')
    parser.add_argument('vectorizer', help='output of vectorizer file (pkl)', type=str, default='model/vectorizer.pkl')
    parser.add_argument('km', help='output of k-means model file (pkl)', type=str, default='model/km.pkl')
    parser.add_argument('X_ar', help='output of vectorized array (npy)', type=str, default='model/X_ar.npy')
    args = parser.parse_args()

    df =  pd.read_pickle(args.cleaned_review)
    (X, vectorizer) = get_reviews_vectorized(df, -1, (1, 2))
    X_ar = X.toarray()
    np.save(args.X_ar, X_ar)
    with open(args.vectorizer, 'wb') as vectorizerfile:
        pickle.dump(vectorizer, vectorizerfile)
    km = kmeans(X_ar=X_ar, random_state=42)
    with open(args.km, 'wb') as kmfile:
        pickle.dump(km, kmfile)