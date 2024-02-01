import numpy as np
import timeit
import pandas as pd
from sklearn import *
import matplotlib.pyplot as plt

df = pd.read_csv("tradelog 11-15-23.csv")

# Remove the last two columns
df.drop(list(df.columns[-3:]), axis=1, inplace=True)
print(df.head())

# only get the execute events and sort by time
df2 = (
    df[df["Event"] == "Execute"]
    .sort_values(by=["Time"], ascending=[True])
    .reset_index(drop=True)  # needed to create a new dataframe not just groupby object
)

print(df2.head(140))

# Dictionary to store temporary P/Ls and number of trades for each symbol
positions = {}

# Dictionary to store P/L and number of trades for each symbol
pl_dict = {"Symbol": [], "P/L": [], "Trades": []}

# Loop
for index, row in df2.iterrows():
    event, bs, symb, shares, price, route, time = row
    if bs == "Buy":
        if symb not in positions:
            positions[symb] = {
                "Shares": shares,
                "P/L": -shares * price,
            }  # PL based on Value of trade
        else:
            positions[symb]["Shares"] += shares
            positions[symb]["P/L"] -= shares * price
    elif bs == "Sell":
        if symb not in positions:
            positions[symb] = {
                "Shares": -shares,
                "P/L": +shares * price,
            }  ##### Implement short #####
        else:
            positions[symb]["Shares"] -= shares
            positions[symb]["P/L"] += shares * price
            if positions[symb]["Shares"] == 0:
                if symb not in pl_dict["Symbol"]:
                    pl_dict["Symbol"].append(symb)
                    pl_dict["P/L"].append(positions[symb]["P/L"])
                    pl_dict["Trades"].append(1)
                else:
                    idx = pl_dict["Symbol"].index(symb)
                    pl_dict["P/L"][idx] += positions[symb]["P/L"]
                    pl_dict["Trades"][idx] += 1
                del positions[symb]

print(positions)  # Empty
print(pl_dict)  # Filled Dict
pl_df = pd.DataFrame(pl_dict)  # Converted to DF
print(pl_df)
