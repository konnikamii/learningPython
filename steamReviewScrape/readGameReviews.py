import pandas as pd

df = pd.read_json('allgamesreviews.json')
print(len(df['game_id'].unique()))
