import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# All with text
# df = pd.read_json(f'filesToIgnore/allreviews.json', lines=True)
# All no text
df = pd.read_json(f'filesToIgnore/allreviews_no_text.json', lines=True)

print(df)
df = df.sample(n=10000)

# # Descriptive Analysis
# average_playtime = df['playtime_at_review'].mean()
# positive_review_proportion = df['voted_up'].mean()
# early_access_review_proportion = df['written_during_early_access'].mean()

# print(f'Average Playtime: {average_playtime}')
# print(f'Proportion of Positive Reviews: {positive_review_proportion}')
# print(f'Proportion of Reviews Written During Early Access: {
#       early_access_review_proportion}')

# received_for_free_counts = df['received_for_free'].value_counts()
# print('\nReceived for Free Counts:')
# print(received_for_free_counts)


# ------------------------- Received free -> Voted up
# ------------------------- Logistic regression and correlation
# Convert boolean columns to integers
df['voted_up'] = df['voted_up'].astype(int)
df['received_for_free'] = df['received_for_free'].astype(int)

# Calculate the percentage of people who voted up for games received for free
free_games_voted_up = df[df['received_for_free'] == 1]['voted_up'].mean() * 100
print(f"Percentage of Voted-Up when received for free: {
      free_games_voted_up}%")

# Calculate the percentage of people who voted up for games not received for free
paid_games_voted_up = df[df['received_for_free'] == 0]['voted_up'].mean() * 100
print(f"Percentage of Voted-Up when NOT received for free: {
      paid_games_voted_up}%")

# Stacked bar plot
cross_tab = pd.crosstab(df['received_for_free'], df['voted_up'])
cross_tab.plot(kind='bar', stacked=True)
plt.title('Received for Free vs Voted Up')
plt.show()

# Correlation
correlation = df[['received_for_free', 'voted_up']].corr()
print(correlation)

# Logistic Regression
X = df[['received_for_free']]
y = df['voted_up']

# X = sm.add_constant(X)  # adding a constant

# model = sm.Logit(y, X)
# result = model.fit()

# print(result.summary())

# # ------------------------- Time Series -> # of Reviews, Avg Playtime, Voted Up
# df['timestamp_created'] = pd.to_datetime(df['timestamp_created'])
# df.set_index('timestamp_created', inplace=True)

# # Time series plot for the number of reviews
# df.resample('ME').size().plot()
# plt.title('Number of Reviews Over Time')
# plt.show()

# # Time series plot for the average playtime at review
# df.resample('ME')['playtime_at_review'].mean().plot()
# plt.title('Average Playtime at Review Over Time')
# plt.show()

# # Time series plot for the proportion of reviews voted up
# df.resample('ME')['voted_up'].mean().plot()
# plt.title('Proportion of Reviews Voted Up Over Time')
# plt.show()


# # ------------------------- Play Time -> # of Reviews, Voted Up
# # Define the bin edges
# bins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000,
#         8000, 9000, 10000, df['playtime_at_review'].max()]

# # Create the bins
# df['playtime_bins'] = pd.cut(
#     df['playtime_at_review'], bins, include_lowest=True)

# # Scatter plot for the number of reviews vs binned playtime at review
# reviews_df = df.groupby('playtime_bins').size().reset_index(name='count')
# reviews_df.plot(kind='bar', x='playtime_bins', y='count')
# plt.title('Number of Reviews vs Binned Playtime at Review')
# plt.show()

# # Scatter plot for the proportion of reviews voted up vs binned playtime at review
# votes_df = df.groupby('playtime_bins')[
#     'voted_up'].mean().reset_index(name='mean')
# votes_df.plot(kind='bar', x='playtime_bins', y='mean')
# plt.title('Proportion of Reviews Voted Up vs Binned Playtime at Review')
# plt.show()
