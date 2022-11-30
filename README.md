# MADS-Capstone: Wine Roadmap Web app

## About the machine learning pipline
1. data_scraper.py: get wine dataset from Vivino.com<br>
Parameter: upper price boundary, lower price boundary, output of wine data, output of review data<br>
Default command:<br>
python data_scraper.py 200 20 asset/wines.pkl asset/reviews.pkl

2. clean_data.py: data cleaning and data processing<br>
Parameter: iutput of wine data, iutput of review data, output of cleaned wine data, output of cleaned review data, output of cleaned review data without text<br>
Default command:<br>
python clean_data.py asset/wines.pkl asset/reviews.pkl asset/cleaned_wines.pkl asset/cleaned_reviews.pkl asset/cleaned_noreviews.pkl

3. model.py: train k-means model<br>
Parameter: input of review data, output of tf-idf vectorizer, output of k-means model, output of transformed array<br>
Default command:<br>
python model.py asset/cleaned_reviews.pkl model/vectorizer.pkl model/km.pkl model/X_ar.npy

## About the Streamlit Pages
1. 1_🍷_Index.py: Introduction and instruction of the Web app
2. 🍇_Flavor.py: Rank the flavors and make a flavor formula to match wines
3. 👍_Recommendation.py: Select favorite wine list to generate the recommended wine list
4. 💭_Wordcloud.py: Visualize the list of wines by making Wordcloud 
5. 🗺️_Visualization.py: Exploring wines with visualizations 
