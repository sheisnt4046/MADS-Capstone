import requests
import math
import re
import pandas as pd
from bs4 import BeautifulSoup
from random import randint
from time import sleep


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
url = 'https://www.vivino.com/'

# Get Cache key to get country codes and type of wines
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
script = soup.find('script', text = re.compile('var vivinoCacheKey'))
vivinoCacheKey = str(script).split('vivinoCacheKey = ')[-1].split(';')[0].replace("'",'').strip()

def get_wine(price_range_max, price_range_min):
    rows = []
    # Iterate through countries and wine types
    api_url = 'https://www.vivino.com/api/explore/explore'
    for country in ['ar', 'pt', 'cl', 'at', 'au', 'es', 'de', 'us', 'it', 'fr']:
        payload = {
        "country_code": country.upper(),
        "currency_code":"USD",
        "grape_filter":"varietal",
        "min_rating":1,
        "min_ratings_count":100,
        "order_by":"ratings_count",
        "order":"desc",
        "page": '1',
        "price_range_max": price_range_max,
        "price_range_min": price_range_min}

        
        jsonData = requests.get(api_url, params=payload, headers=headers).json()
        total_pages = math.ceil(jsonData['explore_vintage']['records_matched'] / 100)
        
        for page in range(1,total_pages+1):
            if page != 1:   
                payload.update({'page':page})
            jsonData = requests.get(api_url, params=payload, headers=headers).json()
            for each in jsonData['explore_vintage']['records']:
                name = f'{each["vintage"]["wine"]["name"]} {each["vintage"]["year"]}'
                year = each["vintage"]["year"]
                id = each["vintage"]["wine"]["id"]
                rating =  each['vintage']['statistics']['ratings_average']
                try:
                    price = each['price']['amount']
                except:
                    price = "None_Supplied"
                winery = each["vintage"]["wine"]["winery"]["name"]
                ratings_count = each["vintage"]["statistics"]["ratings_count"]
                country = country
                try:
                    image = each['vintage']['image']['variations']['bottle_small_square']
                except:
                    image = "None_Supplied"
                try:
                    number_of_flavors_in_wine = int(len(each['vintage']['wine']['taste']['flavor']))
                    flavors_in_wine = []
                    for flavor in range(number_of_flavors_in_wine):
                        flavors_in_wine.append(each['vintage']['wine']['taste']['flavor'][flavor]) #flavor(s)
                except:
                    number_of_flavors_in_wine = "None_Supplied"
                    flavors_in_wine = "None_Supplied"
                
                row = {'name':name, "year":year, "wine ID":id, 'rating':rating, 'price':price, 'winery': winery, 'ratings_count': ratings_count, 'country': country,\
                        'image': image, 'number_of_flavors': number_of_flavors_in_wine, 'flavors_in_wine': flavors_in_wine}
                rows.append(row)
            print('Aquired page: %s - %s/%s ' %(country, page, total_pages))


    df = pd.DataFrame(rows)
    df = df[df.ratings_count>100]
    df = df.drop_duplicates(subset = ['year', 'wine ID'] , keep = 'first')
    return df


def get_wine_data(wine_id, year, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = "https://www.vivino.com/api/wines/{id}/reviews?per_page=50&year={year}&page={page}"  # <-- increased the number of reviews to 9999

    data = requests.get(
        api_url.format(id=wine_id, year=year, page=page), headers=headers
    ).json()

    return data


def get_review_data(df):
    ratings=[]
    for _, row in df.iterrows():
        page = 1
        while True:
            print(
                f'Getting info about wine {row["wine ID"]}-{row["year"]} Page {page}'
                )
            try:
                d = get_wine_data(row["wine ID"], row["year"], page)
            except:
                sleep(10)
                continue

            try:
                for r in d["reviews"]:
                    if r["language"] != "en": # <-- get only english reviews
                        continue

                    ratings.append(
                            [
                                row["wine ID"],
                                row["year"],
                                r["rating"],
                                r["note"],
                                r["created_at"],
                                r['vintage']['wine']['region']['country']['name']
                            ]
                        )
            except:
                break


            if page == 2:
                break

            page += 1


        df_reviews = pd.DataFrame(
            ratings, columns=["wine ID", "year", "User Rating", "Review", "CreatedAt", "country"]
        )

    return df_reviews


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('price_range_max', help='upper boundary of the price', type=int, default=200)
    parser.add_argument('price_range_min', help='lower boundary of the price', type=int, default=20)
    parser.add_argument('wine_data', help='wine data file (pkl)', type=str, default='asset/wines.pkl')
    parser.add_argument('review_data', help='review data file (pkl)', type=str, default='asset/reviews.pkl')
    args = parser.parse_args()

    wine_data = get_wine(args.price_range_max, args.price_range_min)
    wine_data.to_pickle(args.wine_data)
    review_data = get_review_data(wine_data)
    review_data.to_pickle(args.review_data)
    