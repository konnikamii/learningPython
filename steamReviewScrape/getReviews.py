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
batches = ['1-1020', '1021-2040', '2041-3060', '3061-4080',
           '4081-5100', '5101-6120', '6121-7140', '7141-8160', '8161-end']
for b in batches:
    batch = b
    df = pd.read_json(f'./games_separated/games{batch}.json')
    print(f'Processing Batch {batch}...')

    # df['Previous Price'] = df['Previous Price'].apply(
    #     lambda x: float(''.join(filter(str.isdigit, x)))/100 if x else 0)
    # df['Current Price'] = df['Current Price'].apply(
    #     lambda x: 0 if x == 'Free To Play' else float(''.join(filter(str.isdigit, str(x))))/100 if x else 0)
    # df['Discount'] = df['Discount'].apply(lambda x: float(
    #     ''.join(filter(str.isdigit, str(x)))) if x else 0)
    # df['Release Date'] = pd.to_datetime(df['Release Date'], format='%b %d, %Y')
    df['ID'] = df['ID'].astype(int)

    # setting up for the loop
    id_list = df['ID'].tolist()
    total_games = len(id_list)
    review_list = []
    game_review_list = []
    game_num = 0
    previous_len = 0

    for i in range(0, total_games):
        game_num += 1
        game_id = id_list[i]
        url = f"https://store.steampowered.com/appreviews/{
            game_id}?json=1&language={language}&reviews_per_page=5&filter={filters}"
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
                    "game_id": game_id,
                    "review_score_desc": review_score_desc if review_score_desc else 'No review',
                    "total_positive": total_positive if total_positive else 0,
                    "total_negative": total_negative if total_negative else 0,
                    "total_reviews": total_reviews if total_reviews else 0
                }
                with open(f'game_reviews{batch}.txt', 'a') as f:
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
                    url = f"https://store.steampowered.com/appreviews/{
                        game_id}?json=1&language={language}&reviews_per_page={reviews_per_page}&filter={filters}&cursor={cursor}"
                    response2 = requests.get(url)
                    print('  ' + f'Game {game_id}.. game {game_num} of {total_games}.. precessed {iterable} out of {
                          total_requests} reviews... Cursor: {cursor}...')

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
                                # voted_up = reviews[i].get('voted_up')
                                # steam_purchase = reviews[i].get('steam_purchase')
                                # received_for_free = reviews[i].get('received_for_free')
                                # written_during_early_access = reviews[i].get('written_during_early_access')
                                review_dict = {
                                    "game_id": game_id,
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
                                review_list.append(review_dict)
                                list_to_append.append(review_dict)

                        else:
                            print("Failed to get data where success is 0")
                    else:
                        print("Failed to get data:", response.status_code)

                with open(f'reviews{batch}.txt', 'a') as f:
                    f.write(json.dumps(list_to_append) + ',,,,,')
            else:
                print("Failed to get data where success is 0")
        else:
            print("Failed to get data:", response.status_code)
        current_len = len(review_list) - previous_len
        previous_len += current_len
        print(f'Game {game_id} done... Processed {
              current_len} reviews... Proceeding to next game... {game_num} of {total_games} - batch {batch}...')

    with open(f'reviews{batch}.json', 'w') as f:
        json.dump(review_list, f)

    with open(f'game_reviews{batch}.json', 'w') as f:
        json.dump(game_review_list, f)

    # timestamp_created = 1709896425
    # timestamp_updated = 1709896425

    # # Convert the timestamps to datetime
    # datetime_created = datetime.datetime.fromtimestamp(timestamp_created)
    # datetime_updated = datetime.datetime.fromtimestamp(timestamp_updated)

    # print("Created:", datetime_created)
    # print("Updated:", datetime_updated)
