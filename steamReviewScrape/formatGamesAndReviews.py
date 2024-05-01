import json
import pandas as pd
import numpy as np

# ----Format  Games
# df = pd.read_json('filesToIgnore/allgames_no_duplicates.json')
# df1 = pd.read_json('filesToIgnore/allgamesreviews_no_duplicates.json')
# df = df.sort_values(by=['ID'], ascending=True).reset_index(drop=True)
# df1 = df1.sort_values(by=['game_id'], ascending=True).reset_index(drop=True)
# df = df.merge(df1, left_on='ID', right_on='game_id', suffixes=('_df', '_df1'))

# df = df.drop(columns='game_id')
# df['Discount'] = df['Discount'] / 100
# df['Release Date'] = pd.to_datetime(df['Release Date'], unit='ms')
# df['Release Date'] = df['Release Date'].dt.strftime('%B %d, %Y')
# df['Reviews'] = df['Reviews'].str.replace(
#     'No reviews', 'No reviews|0')
# df[['Review Summary', 'Review Number']
#    ] = df['Reviews'].str.split('|', expand=True)
# df['Review Number'] = df['Review Number'].str.replace(',', '')
# df['Review Number'] = pd.to_numeric(df['Review Number'])
# df = df.rename(columns={'review_score_desc': 'API Review Summary',
#                         'total_reviews': 'API Review Number',
#                         'total_positive': 'API Positive Reviews',
#                         'total_negative': 'API Negative Reviews'
#                         })
# df['API Review Summary'] = df['API Review Summary'].replace(
#     '\d+ user reviews', 'Not enough reviews', regex=True)
# df = df[['ID', 'Title', 'Description', 'Discount', 'Previous Price', 'Current Price', 'Categories', 'Release Date', 'Review Summary',
#          'Review Number', 'API Review Summary', 'API Review Number', 'API Positive Reviews', 'API Negative Reviews', 'Link']]
# df2 = pd.read_json('gamesBeta.json', lines=True)
# print(df.dtypes)
# df.to_json('gamesEA.json', orient='records', lines=True)
# print(df2.dtypes)
# # Review score summary
# review_scores = {
#     'Overwhelmingly Positive': 4,
#     'Very Positive': 3,
#     'Positive': 2,
#     'Mostly Positive': 1,
#     'Mixed': 0,
#     'Mostly Negative': -1,
#     'Negative': -2,
#     'Very Negative': -3,
#     'Overwhelmingly Negative': -4,
# }
# df = pd.read_json('gamesEA.json', lines=True)
# print(df.dtypes)

# df['Review Summary Score'] = df['Review Summary'].map(review_scores)
# df = df[['ID', 'Title', 'Description', 'Discount', 'Previous Price', 'Current Price', 'Categories', 'Release Date', 'Review Summary', 'Review Summary Score',
#          'Review Number', 'API Review Summary', 'API Review Number', 'API Positive Reviews', 'API Negative Reviews', 'Link']]
# print(df.dtypes)
# df.to_json('gamesEA.json', orient='records', lines=True)

# ----- Format Reviews
# df1 = df1.rename(columns={
#     'game_id': 'ID',
#     'review': 'Review',
#     'language': 'Language',
#     'playtime_at_review': 'Playtime at Review',
#     'voted_up': 'Voted Up',
#     'steam_purchase': 'Steam Purchase',
#     'received_for_free': 'Received for Free',
#     'written_during_early_access': 'Written During Early Access',
#     'timestamp_created': 'Timestamp Created',
#     'timestamp_updated': 'Timestamp Updated',
# })
# column_order = ['ID', 'Review', 'Language', 'Playtime at Review', 'Voted Up', 'Steam Purchase',
#                 'Received for Free', 'Written During Early Access', 'Timestamp Created', 'Timestamp Updated']

# df1 = df1[column_order]
# df1 = df1.sort_values(by=['ID', 'Timestamp Created'],
#                       ascending=True).reset_index(drop=True)
# print(df1)
# # Write the DataFrame to a new JSON file
# df1.to_json('reviewsEA.json', orient='records', lines=True)


np.random.seed(3218)
# Get game samples
df = pd.read_json('gamesEA.json', lines=True)
df = df.sample(n=65).sort_values(
    by=['ID', 'Release Date']).reset_index(drop=True)
print(df)
df.to_json('gamesEAsample3.json', orient='records', lines=True)

df1 = pd.read_json('reviewsEA.json', lines=True)
df1 = df1[df1['ID'].isin(df['ID'].unique())]
df1 = df1.groupby('ID').apply(lambda x: x.head(2000)).reset_index(drop=True)
print(df1)
df1.to_json('reviewsEAsample3.json', orient='records', lines=True)
