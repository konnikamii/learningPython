import random
import time
import pandas as pd
import requests
import json
from urllib.parse import quote
import math
import datetime

# Setting up the parameters
language = 'english'
reviews_per_page = 100
filters = 'recent'

df = pd.read_json(f'./filesToIgnore/betaGamesFormatted.json')

df['ID'] = df['ID'].astype(int)

# setting up for the loop
# id_list = df['ID'].tolist()
id_list = [322330, 420290, 4000, 1139900, 361420]
total_games = len(id_list)
review_list = []
game_review_list = []
game_num = 0
previous_len = 0
iter = 0
for id in id_list:
    iter = iter+1
    print(f'game {iter} of {len(id_list)}')
    url = f"https://store.steampowered.com/appreviews/{
        id}?json=1&language={language}&num_per_page=5&filter={filters}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['success'] == 1:
            review_score_desc = data['query_summary'].get(
                'review_score_desc')
            total_positive = data['query_summary'].get('total_positive')
            total_negative = data['query_summary'].get('total_negative')
            total_reviews = data['query_summary'].get('total_reviews')
            game_review_dict = {
                "game_id": id,
                "review_score_desc": review_score_desc if review_score_desc else 'No review',
                "total_positive": total_positive if total_positive else 0,
                "total_negative": total_negative if total_negative else 0,
                "total_reviews": total_reviews if total_reviews else 0
            }
            with open(f'gamereviewsBeta.txt', 'a') as f:
                f.write(json.dumps(game_review_dict) + ',\n')
            game_review_list.append(game_review_dict)

            list_to_append = []

            total_requests = math.floor(total_reviews / 100)+1
            if total_requests == 0:
                total_requests = 1
            cursor = '*'
            iterable = 0
            for i in range(0, total_requests):
                iterable += 1
                if len(list_to_append) > 1999:
                    continue
                url = f"https://store.steampowered.com/appreviews/{
                    id}?json=1&language={language}&num_per_page={reviews_per_page}&filter={filters}&cursor={cursor}"
                response2 = requests.get(url)

                time.sleep(random.uniform(0.5, 1.1))
                if response.status_code == 200:
                    try:
                        data2 = response2.json()
                    except json.JSONDecodeError:
                        print("BOM detected... Retrying...")
                        data2 = json.loads(
                            response2.content.decode('utf-8-sig'))
                    if data2['success'] == 1:
                        cursor = data2['cursor']
                        cursor = quote(cursor)
                        reviews = data2['reviews']
                        for i in range(0, len(reviews)):
                            playtime_at_review = reviews[i]['author'].get(
                                'playtime_at_review')
                            if not playtime_at_review:
                                playtime_at_review = reviews[i]['author'].get(
                                    'playtime_forever')
                            language = reviews[i].get('language')
                            review = reviews[i].get('review')
                            timestamp_created = reviews[i].get(
                                'timestamp_created')
                            timestamp_updated = reviews[i].get(
                                'timestamp_updated')
                            review_dict = {
                                "game_id": id,
                                "playtime_at_review": playtime_at_review,
                                "language": language if language else 'all',
                                "review": review if review else 'No review',
                                "timestamp_created": timestamp_created if timestamp_created else 0,
                                "timestamp_updated": timestamp_updated if timestamp_updated else 0,
                                "voted_up": reviews[i].get('voted_up', False),
                                "steam_purchase": reviews[i].get('steam_purchase', False),
                                "received_for_free": reviews[i].get('received_for_free', False),
                                "written_during_early_access": reviews[i].get('written_during_early_access', False)
                            }
                            # with open(f'reviews{batch}.txt', 'a') as f:
                            #     f.write(json.dumps(review_dict) + '\n')
                            # review_list.append(review_dict)
                            list_to_append.append(review_dict)
                        print(len(list_to_append))

                    else:
                        print("Failed to get data where success is 0")
                else:
                    print("Failed to get data:", response.status_code)

            # with open(f'reviewsBeta.txt', 'a') as f:
            #     f.write(json.dumps(list_to_append) + ',\n')

            with open('reviewsBeta.json', 'a') as f:
                for dict_item in list_to_append:
                    f.write(json.dumps(dict_item) + '\n')
        else:
            print("Failed to get data where success is 0")
    else:
        print("Failed to get data:", response.status_code)

# with open(f'reviewsBeta.json', 'w') as f:
#     json.dump(review_list, f)

# with open(f'game_reviewsBeta.json', 'w') as f:
#     json.dump(game_review_list, f)
