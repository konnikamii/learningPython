import pandas as pd

# Read the JSON file into a DataFrame
df = pd.read_json('allgames.json')

df['Previous Price'] = df['Previous Price'].apply(
    lambda x: float(''.join(filter(str.isdigit, x)))/100 if x else 0)

df['Current Price'] = df['Current Price'].apply(
    lambda x: 0 if x == 'Free To Play' else float(''.join(filter(str.isdigit, str(x))))/100 if x else 0)

df['Discount'] = df['Discount'].apply(lambda x: float(
    ''.join(filter(str.isdigit, str(x)))) if x else 0)

# df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Release Date'] = pd.to_datetime(df['Release Date'], format='%b %d, %Y')

df['ID'] = df['ID'].astype(int)

# print(df['Previous Price'])
# print(df['Current Price'])
# print(df['Discount'])
# print(df['Release Date'])
# print(df['ID'])
# print(df['Title'])
# milidor_entry = df.loc[df['Title'] == 'Millidor']
# print(milidor_entry)
# empty_price_entries = df[df['Current Price'] == 0]
# print(empty_price_entries)
print(df)
print(len(df['ID'].unique()))
