import pandas as pd

df = pd.read_json(f'allreviews.json', lines=True)
print(df)
