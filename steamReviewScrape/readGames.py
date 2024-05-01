import sys
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.regressionplots import influence_plot

# Games
# ID                        int64
# Title                    object
# Description              object
# Discount                float64
# Previous Price          float64
# Current Price           float64
# Categories               object
# Release Date             object
# Review Summary           object
# Review Number             int64
# API Review Summary       object
# API Review Number         int64
# API Positive Reviews      int64
# API Negative Reviews      int64
# Link                     object

# Reviews
# ID                                      int64
# Review                                 object
# Language                               object
# Playtime at Review                      int64
# Voted Up                                 bool
# Steam Purchase                           bool
# Received for Free                        bool
# Written During Early Access              bool
# Timestamp Created              datetime64[ns]
# Timestamp Updated              datetime64[ns]

np.random.seed(0)
review_scores = {
    'Overwhelmingly Positive': 4,
    'Very Positive': 3,
    'Positive': 2,
    'Mostly Positive': 1,
    'Mixed': 0,
    'Mostly Negative': -1,
    'Negative': -2,
    'Very Negative': -3,
    'Overwhelmingly Negative': -4,
}
review_scores_labels = {v: k for k, v in review_scores.items()}
positive_review_scores = {v: k for k, v in review_scores.items() if v >= -1}
df = pd.read_json('gamesEAsample3.json', lines=True)
dfSummary = df.describe().drop('ID', axis=1)


df1 = pd.read_json('gamesBeta.json', lines=True)
df1Summary = df1.describe().drop('ID', axis=1)


# ------------- Price
# # Box plot for price
# df_prices = pd.concat([df['Current Price'], df1['Current Price']], axis=1)
# df_prices.columns = ['Current Price EA', 'Current Price Beta']

# print(df_prices)
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=df_prices)
# plt.title('Box plot for Early Access Games')
# plt.show()

# ------------- Categories
# Setup Exploded DFs
df_exploded = df.explode('Categories')
df1_exploded = df1.explode('Categories')
selected_categories = df1_exploded['Categories'].unique().tolist()
df_exploded = df_exploded[df_exploded['Categories'].isin(selected_categories)]

# # Count barchart
# ea_category_counts = df_exploded['Categories'].value_counts()
# beta_category_counts = df1_exploded['Categories'].value_counts()
# category_counts = pd.DataFrame(
#     {'Early Access': ea_category_counts, 'Beta': beta_category_counts}).sort_values(by=['Beta', 'Early Access'])
# category_counts.plot(kind='barh', figsize=(10, 6))
# plt.title('Category Counts for Early Access and Beta Games')
# plt.xlabel('Number of Games')
# plt.ylabel('Category')
# plt.show()


# # Review Score barchart
# ea_category_review_scores = df_exploded.groupby(
#     'Categories')['Review Summary Score'].mean()
# beta_category_review_scores = df1_exploded.groupby(
#     'Categories')['Review Summary Score'].mean()
# category_data = pd.DataFrame(
#     {'Early Access': ea_category_review_scores, 'Beta': beta_category_review_scores}).sort_values(by=['Beta', 'Early Access'])
# category_data.plot(kind='barh', figsize=(10, 6))
# plt.title('Average Review Score per Category for Early Access and Beta Games')
# plt.xlabel('Review Score')
# plt.xticks(list(positive_review_scores.keys()),
#            list(positive_review_scores.values()))
# plt.ylabel('Category')
# plt.show()


# # Review Score crosstab EA
# ea_cross_counts = pd.crosstab(
#     df_exploded['Categories'], df_exploded['Review Summary'])
# ea_cross_counts['Total'] = ea_cross_counts.sum(axis=1)
# ea_cross_counts = ea_cross_counts.sort_values(
#     by='Total', ascending=False).drop(columns='Total')
# ea_cross_counts.plot(kind='barh', stacked=True)
# plt.title(
#     'Cross tabulation for Review Scores per Category for Early Access Games')
# plt.xlabel('Total Games')
# plt.ylabel('Category')
# plt.show()

# # Review Score crosstab Beta
# beta_cross_counts = pd.crosstab(
#     df1_exploded['Categories'], df1_exploded['Review Summary'])
# beta_cross_counts['Total'] = beta_cross_counts.sum(axis=1)
# beta_cross_counts = beta_cross_counts.sort_values(
#     by='Total', ascending=False).drop(columns='Total')
# beta_cross_counts.plot(kind='barh', stacked=True)
# plt.title(
#     'Cross tabulation for Review Scores per Category for Beta Games')
# plt.xlabel('Total Games')
# plt.ylabel('Category')
# plt.show()


# ------------- Reviews
# # Box plot for total reviews
# df_total_reviews = pd.concat(
#     [df['Review Number'], df1['Review Number']], axis=1)
# df_total_reviews.columns = ['Review Number EA', 'Review Number Beta']

# print(df_total_reviews)
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=df_total_reviews)
# plt.title('Box plot for Early Access Games')
# plt.show()

# # Box plot for positive/negative reviews EA
# df_review_sentiment = pd.concat(
#     [df['API Positive Reviews'], df['API Negative Reviews']], axis=1)
# df_review_sentiment.columns = [
#     'API Positive Reviews EA', 'API Negative Reviews EA']
# Q1 = df_review_sentiment.quantile(0.25)
# Q3 = df_review_sentiment.quantile(0.75)
# IQR = Q3 - Q1
# mask = (df_review_sentiment >= (Q1 - 1.5 * IQR)
#         ) & (df_review_sentiment <= (Q3 + 1.5 * IQR))
# df_review_sentiment = df_review_sentiment[mask]
# print(df_review_sentiment)
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=df_review_sentiment)
# plt.title('Box plot for Early Access Games')
# plt.show()

# # Box plot for positive/negative reviews Beta
# df_review_sentiment = pd.concat(
#     [df1['API Positive Reviews'], df1['API Negative Reviews']], axis=1)
# df_review_sentiment.columns = [
#     'API Positive Reviews Beta', 'API Negative Reviews Beta']
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=df_review_sentiment)
# plt.title('Box plot for Early Access Games')
# plt.show()

# # Box plot for review score
# df_review_score = pd.concat(
#     [df['Review Summary Score'], df1['Review Summary Score']], axis=1)
# df_review_score.columns = [
#     'Review Summary Score EA', 'Review Summary Score Beta']
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=df_review_score)
# plt.title('Box plot for Early Access Games')
# plt.yticks(list(review_scores_labels.keys()),
#            list(review_scores_labels.values()))
# plt.show()

# -------------  Realease Date
# Convert the 'Release Date' columns to datetime
df['Release Date'] = pd.to_datetime(df['Release Date'])
df1['Release Date'] = pd.to_datetime(df1['Release Date'])

# Create a figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the histograms
df['Release Date'].hist(ax=ax, bins=30, alpha=0.5, label='Early Access')
df1['Release Date'].hist(ax=ax, bins=30, alpha=0.5, label='Beta')

# Set the title and labels
ax.set_title('Histogram of Release Dates')
ax.set_xlabel('Release Date')
ax.set_ylabel('Frequency')

# Show the legend
ax.legend()

# Show the plot
plt.show()
