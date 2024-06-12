from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
import pandas as pd
import random
import json


# Read Me
# This code creates a selenium driver and scrapes the steam webpage for game data.
# The html page is parsed with beautiful soup to extract the necessary data.
# The page is infinite scroll type and requires a click of a button everytime you reach the end of it.
# This is where selenium does the work.
# Once we have loaded the required number of titles in our html we then append them to a json file.
# The code may not work in its current state based on what the steam web page looks likes and
# whether any changes were made to the structure of the html and the respective classes of the used elements.
###

# Create a new instance of the driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Set up column titles for the Dataframe
df = pd.DataFrame(columns=["Title", "Description", "Discount", "Previous Price",
                           "Current Price", "Categories", "Release Date", "Reviews", "Link", "ID"])
driver.implicitly_wait(10)
iterable = 0
iter = 0
rounds = 0
# Loop could be used for all batches of games
for _ in range(0, 1):
    # Go to the page
    if iterable >= 8288:
        break
    driver.get(
        f"https://store.steampowered.com/genre/Early%20Access/?flavor=contenthub_all&facets13268=11%3A0&offset={1020}")
    iterable += 1020  # 1073
    iterable += 2040  # 2076
    iterable += 3060  # 3094
    iterable += 4080  # 4098
    iterable += 5100  # 5115
    iterable += 6120  # 6127
    iterable += 7140  # 7142
    iterable += 8160  # 8148
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script(
        "window.scrollTo(0, arguments[0]);", total_height * 0.9)
    rounds += 1
    print(f'Round {rounds}')
    for i in range(0, 84):
        button = driver.find_element(
            By.XPATH, "//button[@tabindex='0' and @class='_3d9cKhzXJMPBYzFkB_IaRp Focusable']")
        if button.text == 'Show more':
            driver.execute_script("arguments[0].scrollIntoView();", button)
            time.sleep(random.uniform(1, 1.2))
            driver.execute_script("arguments[0].click();", button)
            iter += 1
            print(f'clicked... {iter}')
            time.sleep(random.uniform(1, 1.2))
        else:
            print('no button found')
            break

    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    games = soup.find_all(class_='_1lRFu670LVk6Gmeb12h7Hr')

    print(len(games))
    print('All games...')

    # try:
    #     with open('games.json', 'r') as f:
    #         list_of_games = json.load(f)
    # except (FileNotFoundError, json.JSONDecodeError):
    list_of_games = []

    for i in range(len(games)):
        game = BeautifulSoup(str(games[i]), 'html.parser')

        title = game.find(
            class_='_3jI467XYJLy1CQ5YZhp2q_ StoreSaleWidgetTitle')
        description = game.find(
            class_='VvP0693dMaft690_o-IeT StoreSaleWidgetShortDesc')
        previous_price = game.find(class_='_1EKGZBnKFWOr3RqVdnLMRN')
        current_price = game.find(class_='Wh0L8EnwsPV_8VAu8TOYr')
        categories = game.find(class_='_3OSJsO_BdhSFujrHvCGLqV')
        all_categories = []
        for i in categories:
            all_categories.append(i.text)
        release_date = game.find(class_='_3eOdkTDYdWyo_U5-JPeer1')
        reviews = game.find(
            class_='_2SbZztpb7hkhurwbFMdyhL _1EmesNUJtSduwwWhSWbO2q')
        if not reviews:
            reviews = game.find(
                class_='_24NyYCjcX9bO4_nfucq3cD ReviewScore Focusable')

        link = game.find('a')
        href = link.get('href')
        parts = href.split('/')
        game_id = parts[4]

        # print('-----------------------------------')
        # print(f'Title: {title.text}')
        # print(f'Description: {description.text}')
        if previous_price:
            discount = game.find(class_='_2fpFvkG2gjtlAHB3ZxS-_7')
        #     print(f'Discount: {discount.text}')
        #     print(f'Previoues price: {previous_price.text}')

        # print(f'Current price: {current_price.text}')
        # print(f'Categories: {all_categories}')
        # print(f'Release date: {release_date.text}')
        # print(f'Reviews: {reviews.text}') if reviews else print(f'No reviews')
        # print(f'Link: {href}')

        game_dict = {
            "Title": title.text,
            "Description": description.text if description else 'No description',
            "Discount": discount.text if previous_price else 0,
            "Previous Price": previous_price.text if previous_price else 0,
            "Current Price": current_price.text if current_price else 0,
            "Categories": all_categories,
            "Release Date": release_date.text,
            "Reviews": reviews.text if reviews else 'No reviews',
            "Link": href,
            "ID": game_id
        }
        list_of_games.append(game_dict)
        with open('games1021-2040retry.json', 'w') as f:
            json.dump(list_of_games, f)

    df2 = pd.DataFrame(list_of_games)
    df = pd.concat([df, df2], ignore_index=True)

    print(df)

# Could be used to import in sql Database
# df.to_sql('my_table', engine, if_exists='replace')
