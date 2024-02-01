import numpy as np
import timeit
import pandas as pd
from sklearn import *
import matplotlib.pyplot as plt
import time

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

print(df2.head(5))
print(df.iloc[:, 0] == "Execute")

# for i, x in df2.items():
#     time.sleep(0.5)
#     print(i)

#     time.sleep(0.5)
#     print(x)
